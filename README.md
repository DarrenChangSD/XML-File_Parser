# XML-File_Parser
> Author: Darren Chang @ UCSD Oncogenomics Lab

This project takes a unique TXT file schema for data from Guardant Health and converts into a CSV file.

## Getting started
> Instructions to run from scratch.

Take all of the .xml files and insert them into a file named "XML-Files". In that same directory make sure all three .py files are in the same directory.

## Which Parser?

For mutation data you will need to run parse_mutation.py but for patient data you will need to run parse_patient.py

```shell
python parse_mutation.py

python parse_patient.py
```
Both commands will generate a CXV file for each TXT file and one CSV file that combines them all. 

## Done!

Currently all the CSV files will populate the current directory. (can work on putting into file to avoid clutter)
