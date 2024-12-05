"""
Type definitions for the contrast-route-duplicates tool.
"""

from typing import TypedDict, Optional, List


class RouteData(TypedDict):
    """Type definition for route data from the Contrast API"""

    signature: str
    vulnerabilities: int
    exercised: Optional[int]
    status: str
    route_hash: str
    route_hash_string: str
    servers_total: int
    critical_vulnerabilities: int


class RouteResponse(TypedDict):
    """Type definition for route API response"""

    success: bool
    messages: List[str]
    routes: List[RouteData]
    count: int
    global_count: int


class EnvConfig(TypedDict, total=True):
    """Type definition for environment configuration"""

    CONTRAST_BASE_URL: str
    CONTRAST_ORG_UUID: str
    CONTRAST_API_KEY: str
    CONTRAST_AUTH: str
