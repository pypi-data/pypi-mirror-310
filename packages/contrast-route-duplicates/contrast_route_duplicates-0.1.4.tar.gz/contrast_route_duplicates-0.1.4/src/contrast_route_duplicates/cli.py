"""
CLI interface for the contrast-route-duplicates tool.
Handles command line argument parsing and orchestration.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich import box

from contrast_route_duplicates.analyzer import RouteAnalyzer
from contrast_route_duplicates.config import load_config
from contrast_route_duplicates.exceptions import ContrastAPIError
from contrast_route_duplicates.utils import write_to_csv

logger = logging.getLogger(__name__)

app = typer.Typer(
    help="Analyze duplicate route signatures in Contrast Security applications"
)
console = Console()


async def analyze_routes(
    app_id: Annotated[str, typer.Argument(help="Application ID to analyze")],
    csv_file: Annotated[
        Optional[Path],
        typer.Option(
            "--csv",
            help="Output results to the specified CSV file",
            dir_okay=False,
            file_okay=True,
            writable=True,
        ),
    ] = None,
    batch_size: Annotated[
        int,
        typer.Option(
            "--batch-size",
            "-b",
            help="Number of routes to fetch per request",
            min=1,
            max=1000,
            show_default=True,
        ),
    ] = 100,
    concurrent_requests: Annotated[
        int,
        typer.Option(
            "--concurrent-requests",
            "-c",
            help="Maximum number of concurrent API requests",
            min=1,
            max=50,
            show_default=True,
        ),
    ] = 10,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose logging")
    ] = False,
) -> None:
    """Analyze route signatures in a Contrast Security application."""
    try:
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=log_level)
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        config = load_config()

        console.print("\n[bold]Starting analysis...[/bold]")

        async with RouteAnalyzer(
            base_url=config["CONTRAST_BASE_URL"],
            org_uuid=config["CONTRAST_ORG_UUID"],
            app_id=app_id,
            api_key=config["CONTRAST_API_KEY"],
            auth=config["CONTRAST_AUTH"],
            batch_size=batch_size,
            max_concurrent=concurrent_requests,
            verbose=verbose,
        ) as analyzer:
            try:
                duplicate_counts = await analyzer.analyze_signature_duplicates()
            except Exception as e:
                error_msg = f"[red bold]Error during analysis:[/red bold] {str(e)}"
                console.print(error_msg)
                raise typer.Exit(1)

            if csv_file:
                write_to_csv(csv_file, duplicate_counts)

            total_routes = sum(count for _, count in duplicate_counts)
            unique_signatures = len(duplicate_counts)
            duplicate_signatures = sum(1 for _, count in duplicate_counts if count > 1)
            duplicate_routes = sum(count - 1 for _, count in duplicate_counts if count > 1)

            console.print("\n")

            summary_table = Table(
                title="Route Analysis Summary",
                show_header=False,
                box=box.ROUNDED,
                min_width=50,
            )

            summary_table.add_column("Metric", style="bold", width=30)
            summary_table.add_column("Value", style="cyan", justify="right", width=20)

            summary_table.add_row("Total routes", f"{total_routes:,}")
            summary_table.add_row("Unique signatures", f"{unique_signatures:,}")
            summary_table.add_row("Signatures with duplicates", f"{duplicate_signatures:,}")
            summary_table.add_row("Total duplicate routes", f"{duplicate_routes:,}")
            summary_table.add_row(
                "Duplicate percentage",
                f"{(duplicate_routes / total_routes * 100):.1f}%",
            )

            console.print(summary_table)

            if csv_file:
                console.print(f"\nDetailed results have been written to: [cyan]{csv_file}[/cyan]")

    except ValueError as e:
        error_msg = f"[red]Configuration error: {str(e)}[/red]"
        console.print(error_msg)
        raise typer.Exit(1)
    except ContrastAPIError as e:
        error_details = f": {e.response_text}" if e.response is not None else ""
        error_msg = f"[red]Error accessing the API: {str(e)}{error_details}[/red]"
        console.print(error_msg)
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        error_msg = f"[red]An error occurred: {str(e)}[/red]"
        console.print(error_msg)
        raise typer.Exit(1)


@app.command()
def analyze(
    app_id: Annotated[str, typer.Argument(help="Application ID to analyze")],
    csv_file: Annotated[
        Optional[Path],
        typer.Option("--csv", help="Output results to the specified CSV file"),
    ] = None,
    batch_size: Annotated[
        int,
        typer.Option(
            "--batch-size", "-b", help="Number of routes to fetch per request"
        ),
    ] = 100,
    concurrent_requests: Annotated[
        int,
        typer.Option(
            "--concurrent-requests",
            "-c",
            help="Maximum number of concurrent API requests",
        ),
    ] = 10,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose logging")
    ] = False,
) -> None:
    """Analyze route signatures in a Contrast Security application."""
    asyncio.run(
        analyze_routes(app_id, csv_file, batch_size, concurrent_requests, verbose)
    )
