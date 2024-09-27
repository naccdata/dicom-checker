"""Test final reporting and exiting."""

import unittest
from unittest.mock import patch

from fw_gear_dicom_checker.finish import report_and_exit


class TestReportAndExit(unittest.TestCase):
    @patch("fw_gear_dicom_checker.finish.sys.exit")
    def test_report_and_exit_with_result(self, mock_exit):
        result = {"file": {"tags": ["tag1", "tag2"]}}

        with patch("fw_gear_dicom_checker.finish.log") as mock_log:
            report_and_exit(result)
            mock_log.info.assert_called_with(
                "Finished DICOM Checker. Resulting tags: %s", result["file"]["tags"]
            )
            mock_exit.assert_called_once_with(0)

    @patch("fw_gear_dicom_checker.finish.sys.exit")
    def test_report_and_exit_without_result(self, mock_exit):
        result = None

        with patch("fw_gear_dicom_checker.finish.log") as mock_log:
            report_and_exit(result)
            mock_log.error.assert_called_with("Finished DICOM Checker. No result.")
            mock_exit.assert_called_once_with(1)

    @patch("fw_gear_dicom_checker.finish.sys.exit")
    def test_report_and_exit_without_tags(self, mock_exit):
        result = {
            "file": {
                "info": {"header": {"dicom": {"FileMetaInformationGroupLength": 206}}},
            }
        }

        with patch("fw_gear_dicom_checker.finish.log") as mock_log:
            report_and_exit(result)
            mock_log.info.assert_called_with("Finished DICOM Checker.")
            mock_exit.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
