"""
Utility functions for the contrast-route-duplicates tool.
"""

import csv
import logging
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


def write_to_csv(output_file: Path, counts: List[Tuple[str, int]]) -> None:
    """Write route signature counts to a CSV file"""
    logger.info(f"Writing results to {output_file}")

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Signature", "Count"])
        writer.writerows(counts)

    logger.info(f"Successfully wrote results to {output_file}")
