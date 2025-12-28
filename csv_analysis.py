import csv
import statistics
import json
import argparse
import os

DEBUG = False
CONFIG_FILE = "./config/columns.json"

def load_config(config_path):
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
    else:
        print(f"Config file ${config_path} not found")
        exit(1)

def load_csv_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            data = [row for row in reader]
            if DEBUG:
                print(f"{len(data)} rows loaded from {file_path}")

        cleaned_data = []
        for row in data:
            cleaned_row = {k.replace('\ufeff', ''): v for k, v in row.items()}
            cleaned_data.append(cleaned_row)

        return cleaned_data
    else:
        print(f"CSV file ${file_path} not found")
        exit(1)

def get_column_name(data, column_identifier):
    try:
        index = int(column_identifier)
        if index < len(data[0].keys()):
            return list(data[0].keys())[index]
        else:
            print(f"Index {index} is out of range.")
            exit(1)
    except ValueError:
        return column_identifier

def convert_to_numerical(data, column_name, mapping):
    text_responses = []
    numerical_data = []
    for row in data:
        text_response = row.get(column_name, '')
        text_responses.append(text_response)
        numerical_data.append(mapping.get(text_response, 0))

    sorted_numbers = sorted(numerical_data, reverse=True)
    if DEBUG:
        print(f"Data as text: {text_responses}")
        print(f"Numerical data: {numerical_data}")
    print(f"Sorted data: {sorted_numbers}")

    return numerical_data

def calculate_statistics(numerical_data):
    if not numerical_data:
        return None

    stats = {
        "mean": statistics.mean(numerical_data),
        "median": statistics.median(numerical_data),
        "mode": statistics.mode(numerical_data),
        "stdev": statistics.stdev(numerical_data) if len(numerical_data) > 1 else 0
    }
    return stats

def main():
    parser = argparse.ArgumentParser(description='Analysis of csv data.')
    parser.add_argument('--csv_file', required=True, type=str, help='Path to CSV file')
    parser.add_argument(
        "--config_file",
        type=str,
        default=CONFIG_FILE,
        help=f"Path to the config JSON file (default: ${CONFIG_FILE})"
    )
    parser.add_argument('--column', required=True, type=str, help='Name or index of column to analyze')
    parser.add_argument('--column_type', required=True, type=str, help='Type of columns for data analysis')
    parser.add_argument('--debug', action='store_true', help='Prints extra debugging information')
    args = parser.parse_args()

    DEBUG = args.debug

    data = load_csv_data(args.csv_file)

    column_name = get_column_name(data, args.column)
    if not column_name:
        print(f"Column '{args.column}' not found.")
        return

    config = load_config(args.config_file)

    column_config = next((col for col in config['columns'] if col['name'] == args.column_type), None)
    if not column_config:
        print(f"Configuration '{args.column_type}' not found in config file.")
        return

    numerical_data = convert_to_numerical(data, column_name, column_config['mapping'])

    stats = calculate_statistics(numerical_data)

    print(f"Statistical analysis for column '{column_name}':")
    print(f"Mean value: {stats['mean']}")
    print(f"Median: {stats['median']}")
    print(f"Modus: {stats['mode']}")
    print(f"standard deviation: {stats['stdev']}")

if __name__ == "__main__":
    main()
