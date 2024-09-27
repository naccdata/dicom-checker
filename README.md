# dicom-checker (DICOM Checker)

## Overview

*[Usage](#usage)*

*[FAQ](#faq)*

### Summary

This gear opens a DICOM file, checks some of the DICOM tags, and then set a Flywheel tag on the input file based on whether the checks pass or fail. The gear checks are configurable.

### License 

*License:* *MIT*

### Classification

*Category:* *utility*

*Gear Level:*

- [ ] Project
- [ ] Subject
- [ ] Session
- [x] Acquisition
- [ ] Analysis

----

[[_TOC_]]

----

### Inputs

- *dicom_file*
  - __Type__: *file*
  - __Optional__: *no*
  - __Description__: *File to check*

- *override_checks*
  - __Type__: *yaml file*
  - __Optional__: *yes*
  - __Description__: *A set of DICOM tags to use instead of the defaults*

### Config

- *debug*
  - __Type__: *boolean*
  - __Description__: *Log debug messages*
  - __Default__: *False*

- *tag_prefix*
  - __Type__: *string*
  - __Description__: *Append '-pass' or '-fail' to <tag_prefix> to generate the Flywheel tag to be placed on the input file.*
  - __Default__: *dicom-checker*

### Outputs

#### Files

*None*

#### Metadata

*None*

#### Tags

The input file will be tagged based on the tag_prefix configuration parameter and if the checks pass or fail.

### Pre-requisites

*None*

#### Prerequisite Gear Runs

*None*

#### Prerequisite Files

*None*

#### Prerequisite Metadata

*None*

## Usage

This gear should be run by a gear rule to check what kind of file the input file is and
tag the result to allow further processing.

### Description

This gear uses the fw-classification library to look for DICOM tags as defined by the default profile which can be overridden by a provide profile file.  That profile should result in the input file being given a Flywheel tag that can trigger further processing.

#### File Specifications

##### *{dicom_file}*

A DICOM file to check.

##### *{override_checks}*

A YAML file to use instead of default.yaml.  See that file for the proper format and also [CT-override.yaml](https://gitlab.com/flywheel-io/scientific-solutions/gears/dicom-checker/-/blob/main/fw_gear_dicom_checker/CT-override.yaml?ref_type=heads) for another example.  All features of the [classification library](https://flywheel-io.gitlab.io/scientific-solutions/lib/fw-classification/) can be used.

### Workflow

1. Create a classification profile file if you want to override the default.  See [fw-classification](https://flywheel-io.gitlab.io/scientific-solutions/lib/fw-classification/) for more information.  The default.yaml file shows the format necessary to use the [Jinja templating engine](https://jinja.palletsprojects.com/) to allow the gear to put the tag_prefix configuration parameter into the Flywheel tag that will be placed on the input file.
1. Upload the override profile to the project so that it can be used as an input to the gear in a gear rule.
1. Set up a gear rule so the dicom-checker gear will run when a file appears.
   1. Set the override_checks input to your profile or leave it empty to use the default profile.
   1. Set the tag_prefix configuration string or leave it blank to use the default, "dicom-checker".  "-pass" or "-fail" will be added to this string to create the tag that will be placed on the input file.  This functionality is provided by the classification profile.
1. When a file appears the dicom-checker gear will:
   1. Run the Jinja templating engine on the classification profile to substitute the tag_prefix configuration parameter into the profile.  
   2. Call the fw-classification library to check the DICOM tags in the input file and perform whatever actions are specified in the profile.
   3. Update the input file's metadata to apply the tag in the profile to the input file.

### Logging

The gear logs the tag that is the result of the classification profile.

## FAQ

[FAQ.md](FAQ.md)

## Contributing

[For more information about how to get started contributing to that gear,
checkout [CONTRIBUTING.md](CONTRIBUTING.md).]
<!-- markdownlint-disable-file -->
