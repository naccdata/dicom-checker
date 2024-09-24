#!/usr/bin/env python
"""Final logging and exit."""

import logging
import sys
from typing import Optional, Dict, Any


log = logging.getLogger(__name__)


def report_and_exit(result: Optional[Dict[str, Any]]) -> None:  # pragma: no cover
    if result:
        if "file" in result and "tags" in result["file"]:
            log.info(
                "Finished DICOM Checker. Resulting tags: %s", result["file"]["tags"]
            )
        else:
            log.info("Finished DICOM Checker.")

        sys.exit(0)

    else:
        log.error("Finished DICOM Checker. No result.")
        sys.exit(1)
