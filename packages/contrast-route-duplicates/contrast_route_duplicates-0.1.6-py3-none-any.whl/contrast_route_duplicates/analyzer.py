"""
Core analyzer class for processing route data from the Contrast Security API.
"""

import asyncio
import logging
import math
import sys
from collections import Counter
from datetime import datetime
from typing import List, Tuple, Optional, Any, Type, Final, Dict, AsyncIterator, Sequence, cast

import httpx
from tqdm.asyncio import tqdm

from contrast_route_duplicates.models import RouteResponse, RouteData
from contrast_route_duplicates.exceptions import ContrastAPIError
from contrast_route_duplicates.resilient import (
    EnhancedAsyncClient,
    TimeoutConfig,
    APIRateLimiter
)

logger = logging.getLogger(__name__)

class RouteAnalyzer:
    """Analyzes route data from the Contrast Security API"""
    
    def __init__(
        self,
        base_url: str,
        org_uuid: str,
        app_id: str,
        api_key: str,
        auth: str,
        batch_size: int = 25,
        max_concurrent: int = 10,
        verbose: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.org_uuid = org_uuid
        self.app_id = app_id
        self.batch_size = batch_size
        self.verbose = verbose
        self.headers: Final[Dict[str, str]] = {
            "accept": "application/json",
            "content-type": "application/json",
            "API-Key": api_key,
            "Authorization": auth,
        }

        # Enhanced client configuration
        timeout_config = TimeoutConfig(
            connect_timeout=10.0,
            read_timeout=30.0,
            write_timeout=10.0,
            pool_timeout=10.0
        )
        
        rate_limiter = APIRateLimiter(requests_per_second=10.0)
        
        self.client = EnhancedAsyncClient(
            timeout_config=timeout_config,
            rate_limiter=rate_limiter,
            headers=self.headers,
            follow_redirects=True,
            limits=httpx.Limits(
                max_keepalive_connections=max_concurrent,
                max_connections=max_concurrent
            ),
        )
        
        self.semaphore = asyncio.Semaphore(max_concurrent)
        logger.debug(f"Initialized RouteAnalyzer for app {app_id}")

    async def __aenter__(self) -> "RouteAnalyzer":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        await self.client.aclose()

    async def get_total_routes(self) -> int:
        """Get the total number of routes for pagination planning"""
        try:
            response_data = await self.get_routes(0, 1)
            return response_data.get("global_count", 0)
        except Exception as e:
            logger.error(f"Error getting total routes count: {e}")
            raise

    async def get_routes(self, offset: int = 0, limit: int = 25) -> RouteResponse:
        """Fetch a page of routes from the API"""
        url = f"{self.base_url}/api/ng/{self.org_uuid}/applications/{self.app_id}/route"
        params: Dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "expand": "skip_links,filterExceptSessionMetadata",
            "sort": "-exercised",
            "quickFilter": "ALL",
        }

        async with self.semaphore:
            response = None
            try:
                response = await self.client.get(url, params=params)
                if response is not None:
                    response.raise_for_status()
                    data: RouteResponse = cast(RouteResponse, response.json())
                    return data
                raise ContrastAPIError("No response received")
            except httpx.HTTPError as e:
                error_text: str = response.text if response is not None else "No response content"
                logger.error(f"HTTP error occurred: {e}")
                logger.error(f"Response content: {error_text}")
                raise ContrastAPIError(str(e), response)

    async def get_routes_concurrently(
        self, total_routes: int
    ) -> AsyncIterator[RouteData]:
        """Fetch routes concurrently in batches"""
        total_pages = math.ceil(total_routes / self.batch_size)

        async def fetch_batch(page: int) -> List[RouteData]:
            offset = page * self.batch_size
            response = await self.get_routes(offset, self.batch_size)
            return response.get("routes", [])

        # Create progress bar
        pbar = tqdm(
            total=total_routes,
            desc="Fetching routes",
            unit="routes",
            file=sys.stdout,
            disable=not self.verbose,
        )

        semaphore_value = self.semaphore._value
        # Process pages in batches
        for batch_start in range(0, total_pages, semaphore_value):
            batch_end = min(batch_start + semaphore_value, total_pages)
            batch_tasks = [fetch_batch(page) for page in range(batch_start, batch_end)]

            try:
                # Wait for batch to complete
                batch_results: Sequence[List[RouteData]] = await asyncio.gather(
                    *batch_tasks
                )

                # Process results
                for routes in batch_results:
                    pbar.update(len(routes))
                    for route in routes:
                        yield route
            except Exception as e:
                logger.error(f"Error processing batch {batch_start}-{batch_end}: {e}")
                raise

        pbar.close()

    async def analyze_signature_duplicates(self) -> List[Tuple[str, int]]:
        """Count duplicate signatures across all routes"""
        signatures: List[str] = []
        total_processed = 0
        start_time = datetime.now()

        try:
            # Get total route count first
            total_routes = await self.get_total_routes()
            logger.info(f"Found {total_routes} total routes to process")

            async for route in self.get_routes_concurrently(total_routes):
                signatures.append(route["signature"])
                total_processed += 1

            end_time = datetime.now()
            duration = end_time - start_time
            logger.info(f"Processed {total_processed} routes in {duration}")

            # Count duplicates using Counter
            signature_counts = Counter(signatures)
            logger.debug(f"Found {len(signature_counts)} unique signatures")

            # Sort by count in descending order, then alphabetically by signature
            sorted_counts = sorted(signature_counts.items(), key=lambda x: (-x[1], x[0]))

            duplicates = [(sig, count) for sig, count in sorted_counts if count > 1]
            logger.info(f"Found {len(duplicates)} signatures with duplicates")

            return sorted_counts
        except Exception as e:
            logger.error(f"Error analyzing signature duplicates: {e}")
            raise
