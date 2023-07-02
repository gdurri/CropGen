import os
import csv
import json
import sys

def remove_strange_characters(s):
    # Define the set of characters you want to allow in the CSV file
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,")
    
    # Filter out any characters not present in the allowed set
    filtered_string = ''.join(filter(allowed_characters.__contains__, s))
    
    return filtered_string

def csv_to_json(csv_file, json_file):
    data = {"EnvironmentTypes": []}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader((remove_strange_characters(line) for line in file))
        for row in reader:
            environment_type = {
                "SimulationName": row['SimulationName'],
                "Season": int(row['Season']),
                "EnvironmentType": int(row['EnvType'])
            }
            data['EnvironmentTypes'].append(environment_type)

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':

    # Example usage:
    # python environment_type_csv_convert.py data\\Dalby_ET1.csv

    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    # Get the directory path of the currently running script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_filename = os.path.basename(csv_file)

    # Create the output directory if it doesn't exist
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Create the JSON file path by prepending the output directory to the base name of the CSV file
    json_file = os.path.join(output_dir, os.path.splitext(csv_filename)[0] + '.json')

    csv_to_json(csv_file, json_file)
