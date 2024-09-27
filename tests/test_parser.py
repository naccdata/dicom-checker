"""Module to test parser.py"""

from pathlib import Path
from unittest.mock import MagicMock

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_dicom_checker.parser import parse_config


def test_parse_config_works():
    """Test"""
    gear_context = MagicMock(spec=GearToolkitContext)
    gear_context.get_input.return_value = "dicom file"
    gear_context.get_input_path.return_value = "somewhere"
    gear_context.output_dir = Path("/output/shmoutput")
    gear_context.config = {
        "tag_prefix": "tag_prefix",
    }

    dicom_file, profile_path, tag_prefix = parse_config(gear_context)

    assert gear_context.get_input.call_count == 1
    assert gear_context.get_input_path.call_count == 1
    assert dicom_file == "dicom file"
    assert profile_path == Path("somewhere")
    assert tag_prefix == "tag_prefix"


def test_parse_config_no_profile_works():
    """Test"""
    gear_context = MagicMock(spec=GearToolkitContext)
    gear_context.get_input.return_value = "dicom file"
    gear_context.get_input_path.return_value = None
    gear_context.output_dir = Path("/output/shmoutput")
    gear_context.config = {
        "tag_prefix": "tag_prefix",
    }

    dicom_file, profile_path, tag_prefix = parse_config(gear_context)

    assert gear_context.get_input.call_count == 1
    assert gear_context.get_input_path.call_count == 1
    assert dicom_file == "dicom file"
    assert profile_path.parts[-2:] == ("fw_gear_dicom_checker", "default.yaml")
    assert tag_prefix == "tag_prefix"
