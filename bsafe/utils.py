import logging
import sys
import time
from pathlib import Path

logger = logging.getLogger(__name__)


def wait_download(filename: str) -> None:
    """Wait for download of a file

    Args:
        filename (str): The name of a downloaded file.
    """
    elapsed = 0
    timeout_sec = 20
    has_timed_out = True
    while elapsed < timeout_sec:
        time.sleep(1)
        downloaded_file_path = Path.home() / "Downloads" / filename
        if downloaded_file_path.exists():
            has_timed_out = False
            break
        elapsed += 1

    if has_timed_out:
        logger.info(f"Download of {filename} has timed out")
        sys.exit(1)
    else:
        logger.info(f"Download of {filename} has been successful")
