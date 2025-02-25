# csv2md

A simple Python utility for converting CSV files to Markdown tables.

## Overview

csv2md is a command-line tool that converts CSV (Comma-Separated Values) data into Markdown formatted tables. It can read from files or standard input and output to files or standard output.

## Usage
```python
# Basic usage with input file
./csv2md.py input.csv

# Using standard input
cat input.csv | ./csv2md.py

# Specifying output file
./csv2md.py input.csv -o output.md

# Using a custom delimiter (e.g., tab)
./csv2md.py input.csv -d $'\t'
```

## Examples
```csv
Name,Age,City
John,25,New York
Jane,30,San Francisco
```

```md
| Name | Age | City |
| --- | --- | --- |
| John | 25 | New York |
| Jane | 30 | San Francisco |
```