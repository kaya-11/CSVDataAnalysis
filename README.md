# CSV Data Analysis Tool

A Python script to analyze CSV data by converting text responses to numerical values and calculating basic statistics.

---

## Features

- Load CSV data (semicolon-separated).
- Convert text responses to numerical values based on a config file.
- Calculate statistics (mean, median, mode, standard deviation).
- Debug mode for extra output.

## Requirements

- Python 3.x
- No additional libraries required (uses built-in modules: `csv`, `statistics`, `json`, `argparse`, `os`).

## Usage

```bash
python3 csv_analysis.py --csv_file <path_to_csv> --column <column_name_or_index> --column_type <column_type>
```

---

## Specifying the Column to Analyze
You can identify the column you want to analyze in one of two ways:


### By Column Name
Provide the exact name of the column as it appears in your CSV file.
Example: --column MyColumn

### By Column Index (1-based)
Provide the index of the column, starting from 1 (not 0).
Example: --column 3 refers to the third column in the CSV file.

### Example Usage

To analyze the column named MyColumn:
```bash
python3 csv_analysis.py --csv_file data.csv --column MyColumn --column_type Probability
```

To analyze the third column (index 3):
```bash
python3 csv_analysis.py --csv_file data.csv --column 3 --column_type Probability
```

### Notes

If you use an index, ensure it is within the valid range of columns in your CSV file.
If you use a name, ensure it matches the column name exactly (including case and special characters).

---

## Configuration Guide

The script uses a **JSON configuration file** to map text responses (e.g., survey answers) to numerical values for statistical analysis. This guide explains the structure and usage of the config file.

### Config File Structure

The config file is a JSON file with a `columns` array. Each entry in `columns` defines a **column type** (e.g., `Satisfaction`, `Probability`) and a **mapping** of text responses to numerical values.

*Example Config File (`columns.json`)*

```json
{
  "columns": [
    {
      "name": "Satisfaction",
      "mapping": {
        "very satisfied": 5,
        "satisfied": 4,
        "neutral": 3,
        "dissatisfied": 2,
        "very dissatisfied": 1
      }
    },
    {
      "name": "Probability",
      "mapping": {
        "very likely": 5,
        "likely": 4,
        "neutral": 3,
        "unlikely": 2,
        "very unlikely": 1
      }
    }
  ]
}
```

### Key Components

#### columns
An array of objects, where each object defines a column type and its mapping rules.

#### name

Type: String
Description: The name of the column type (e.g., Satisfaction, Probability).
Usage: This name is referenced in the --column_type argument when running the script.

#### mapping

Type: Object (dictionary)
Description: Maps text responses (keys) to numerical values (values).

*Example:*

```json
"mapping": {
  "very satisfied": 5,
  "satisfied": 4
}
```

The text "very satisfied" will be converted to the numerical value 5.

### How to Use the Config File

Default Location:
The script looks for the config file at ./config/columns.json by default.
You can override this path using the --config_file argument:

```bash
python3 app.py --config_file /path/to/your/config.json ...
```

### Adding New Column Types:
To add a new column type (e.g., Frequency), add an entry to the columns array:

```json
{
  "name": "Frequency",
  "mapping": {
    "always": 5,
    "often": 4,
    "sometimes": 3,
    "rarely": 2,
    "never": 1
  }
}
```

### Modifying Mappings:
Edit the mapping object to change how text responses are converted to numerical values.
For example, to use a 10-point scale for Satisfaction:

```json
"mapping": {
  "very satisfied": 10,
  "satisfied": 8,
  "neutral": 5,
  "dissatisfied": 2,
  "very dissatisfied": 0
}
```
