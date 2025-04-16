# bento-data-generator
This is the user documentation for the synthetic data generator for the CRDC data commons.

## Introduction
The synthetic data generator is a Python application used to generate synthetic data based on the CRDC data models(GC, ICDC, CTDC)

The synthetic data generator can be found in this Github Repository: [bento-data-generator](https://github.com/CBIIT/bento-data-generator)

## Pre-requisites
* Python 3.6 or newer

## Dependencies
Run ```pip3 install -r requirements.txt``` to install dependencies. Or run ```pip install -r requirements.txt``` if you are using virtualenv. The dependencies included in ````requirements.txt```` are listed below:

* pandas
* pyyaml
* openpyxl
* requests
* neo4j
* xlsxwriter

## Inputs
* A synthetic data generator configuration file

## Outputs
The synthetic data generator generates a set of synthetic mock data files based on the given CRDC data model and stores them in the specified folder in TSV format.

## Configuration File
All the inputs of the synthetic data generator can be set in a YAML format configuration file by using the fields defined below. 

An example configuration file can be found in ````configuration_files_cds_5.0.0.yaml````

* ````NODE_FILE````: The YAML format model file for the CRDC data model.
* ````PROP_FILE````: The YAML format model properties file for the CRDC data model.
* ````SYNTHETIC_DATA_FILE````: The EXCEL format file for the user to add the custom values to specified properties in the generated synthetic dataset.
* ````DATA_SPEC_FILE````: The detailed configuration file for the custom data generation.
* ````ID_FILE````: The YAML format file with ID fields for each node from the data model file.
* ````OUTPUT_FOLDER````: The directory for the output synthetic mock data files.
* ````GET_CDE_PERMISSIVE_VALUES````: The boolean value determines whether or not to get the permissive values from the given CDE code instead of using the permissive values from the data model.
* ````CDE_ENV````: The datahub environment for getting the CDE permissive values.
* ````CDE_PERMISSIVE_URL````: The address of the datahub permissive values API.
* ````DELETE_ERROR_FILE````:  The boolean value determines whether or not to delete the generated synthetic mock data files if the validation fails.
* ````NON_PERMISSIVE_VALUE````: The boolean value determines whether or not to generate non_permissive values.

In the configuration file, ````DATA_SPEC_FILE```` value is the detailed configuration file for customizing the mock data generation. An example ````DATA_SPEC_FILE```` can be found in ````cds_configuration_files_5.0.0/cds-mock-data-specs.yaml````.


# Command Line Arguments


* **Configuration File**
    * The YAML file containing the configuration details for the synthetic data generator
    * Command : ````<configuration file>````
    * Not Required
    * Default Value : ````N/A````

## Usage Example

The user can use the command listed below to run the python script for generating Bento data in the local machine, 
```python bento-synthetic-data-generator.py configuration_files_bento.yaml```