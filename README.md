# ORD Schema Repository
A repository for healthcare data schemas based on the [Open mHealth schema specification](http://www.openmhealth.org/documentation/#/schema-docs/overview). This repository was initially forked from the [Open mHealth schemas repository](https://github.com/openmhealth/schemas) and has since been extended to support additional schema types and use cases, including ROS4HC [Ros4HC repository](https://github.com/SCAI-Lab/ros4healthcare.git).

In addition to the schemas, the repository includes:

- Sample test data  
- A data validator  
- A Java-based schema SDK

[![Test Data Validator Status](https://github.com/openmhealth/schemas/actions/workflows/validator.yaml/badge.svg)](https://github.com/openmhealth/schemas/actions/workflows/validator.yaml)

## Schemas
Schemas are located in the [`schema`](schema) directory, organized into two main categories:

- **Open mHealth Schemas** – standard schemas from the Open mHealth initiative  
- **ROS4HC Schemas** – extensions and additions developed for the ROS4HC project

## WIKI
Detailed documentation and usage instructions can be found in the [project wiki](wiki).

## Tools Included

- **Validator** – to verify schema compliance of sample data  
- **Java SDK** – for working with schemas in Java-based projects  
- **Sample Data** – to demonstrate schema structure and test validation
