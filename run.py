#!/usr/bin/env python
"""The run script."""

import logging

from flywheel_gear_toolkit import GearToolkitContext

# This design with a separate main and parser module
# allows the gear to be publishable and the main interfaces
# to it can then be imported in another project which enables
# chaining multiple gears together.
from fw_gear_dicom_checker.parser import parse_config
from fw_gear_dicom_checker.main import run
from fw_gear_dicom_checker.finish import report_and_exit

# The run.py should be as minimal as possible.
# The gear is split up into 2 main components. The run.py file which is executed
# when the container runs. The run.py file then imports the rest of the gear as a
# module.


log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse gear config and run."""
    # Call parse_config to extract the args, kwargs from the context
    # (e.g. config.json).
    dicom_file, profile_path, tag_prefix = parse_config(context)

    # Pass the args, kwargs to fw_gear_dicom_checker.main.run function to execute
    # the main functionality of the gear.
    result = run(dicom_file, profile_path, tag_prefix)

    if result:
        context.metadata.update_file_metadata(
            dicom_file, True, "acquisition", **result["file"]
        )

    report_and_exit(result)


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()

        # Pass the gear context into main function defined above.
        main(gear_context)
