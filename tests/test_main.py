"""Module to test main.py"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from fw_gear_dicom_checker.main import run

INITIAL_METADATA = {
    "file": {
        "info": {"header": {"dicom": {"FileMetaInformationGroupLength": 206}}},
        "type": "dicom",
        "tags": ["im-just-a-tag"],
    }
}

RETURNED_METADATA = {
    "file": {
        "type": "dicom",
        "tags": ["im-just-a-tag"],
    }
}

INSTANTIATED_PROFILE = """---
name: MR tagger

profile:
  - name: Magnetic Resonance
    description: |
      Set tag if Modality is MR
    variables:
      fihd: file.info.header.dicom
      ft: file.tags
    rules:
      - match_type: all
        match:
          - key: $fihd.Modality
            is: MR
        action:
          - key: $ft
            add: "some-stringy-string-pass"
      - match_type: all
        match:
          - not:
              - key: $fihd.Modality
                is: MR
        action:
          - key: $ft
            add: "some-stringy-string-fail\""""


class Adapter:
    def __init__(self, file) -> None:
        """Initialize adapter with file."""
        self.file = file

    def classify(self, arg):
        return INITIAL_METADATA


@patch("fw_gear_dicom_checker.main.available_adapters")
def test_run(mock_adapter):
    """run"""

    mock_adapter.__getitem__.side_effect = {"dicom": Adapter}.__getitem__

    dicom_file = {
        "object": {"type": "dicom"},
        "location": {"path": "whatever"},
    }
    MagicMock()
    profile_path = (
        Path(__file__).resolve().parent.parent / "fw_gear_dicom_checker/default.yaml"
    )

    result = run(dicom_file, profile_path, "some-stringy-string")

    assert result == RETURNED_METADATA

    instantiated = (
        Path(__file__).resolve().parent.parent
        / "fw_gear_dicom_checker/instantiated_profile.yaml"
    )
    instantiated_text = instantiated.read_text()

    assert instantiated_text == INSTANTIATED_PROFILE
