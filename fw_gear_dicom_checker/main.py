"""Main module."""

import logging
import typing as t
from pathlib import Path
from jinja2 import Template

from fw_classification.adapters import Adapter
from fw_classification import available_adapters

log = logging.getLogger(__name__)


def run(
    dicom_file: t.Dict[str, t.Any],
    profile_path: Path,
    tag_prefix: str,
) -> t.Dict[str, t.Any]:
    """Run classification via fw-classification.

    This function is more or less a wrapper around the classification-toolkit
    [fw-classification](https://gitlab.com/flywheel-io/public/classification-toolkit),
    with a few gear specific additions.

    1. Set up DICOM fw-classification adapter
    2. Run classification

    Args:
        dicom_file: Flywheel file object.
        profile_path: Path to profile file.
        tag_prefix: Prefix to substitute into profile.

    Returns:
        t.Dict[str, t.Any]: metadata to update file, etc. with.
    """
    log.info("Starting DICOM Checker.")

    # substitute tag_prefix in profile, even if it's not the default which may not have "{{ tag_prefix }}" in it
    template = Template(profile_path.read_text())
    instantiated_profile = template.render(tag_prefix=tag_prefix)
    instantiated_profile_path = profile_path.parent / "instantiated_profile.yaml"
    instantiated_profile_path.write_text(instantiated_profile)

    # call classifier
    cls: t.Type[Adapter] = available_adapters["dicom"]
    classifier = cls(dicom_file["location"]["path"])
    result = classifier.classify(instantiated_profile_path)

    return result
