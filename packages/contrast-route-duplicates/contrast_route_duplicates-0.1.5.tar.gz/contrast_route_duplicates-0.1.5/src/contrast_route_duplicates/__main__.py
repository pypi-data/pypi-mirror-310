"""
Entry point for the contrast-route-duplicates package.
"""

import sys
from pathlib import Path

# Add the parent directory to PYTHONPATH
package_dir = str(Path(__file__).resolve().parent.parent)
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from contrast_route_duplicates.cli import app

if __name__ == "__main__":
    app()
