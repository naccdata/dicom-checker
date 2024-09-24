"""Parser module to parse gear config.json."""

import logging
from pathlib import Path
from typing import Tuple, Any, Optional, Dict

from flywheel_gear_toolkit import GearToolkitContext


log = logging.getLogger(__name__)


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[Dict[str, Any], Path, str]:
    """Parse gear config.json.

    Args:
        gear_context (GearToolkitContext): Gear context object

    Returns:
        Tuple[Dict[str, Any], Path, str]: dicom_file, profile_path, tag_prefix
    """
    dicom_file: Dict[str, Any] = gear_context.get_input("dicom_file")

    profile_path: Optional[Path] = gear_context.get_input_path("override_checks")
    if profile_path:
        log.info(f"Using profile from input {profile_path}")
        profile_path = Path(profile_path)
    else:
        log.info("Using default profile")
        profile_path = Path(__file__).resolve().parent / "default.yaml"

    profile_path.parts[-2:]
    tag_prefix = gear_context.config["tag_prefix"]

    return dicom_file, profile_path, tag_prefix
