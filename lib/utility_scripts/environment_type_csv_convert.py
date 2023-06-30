import os
import csv
import json
import sys

def csv_to_json(csv_file, json_file):
    data = {"EnvironmentTypes": []}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
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
    csv_filename = os.path.basename(csv_file)
    json_file = os.path.splitext(csv_filename)[0] + '.json'

    if not json_file.startswith('output/'):
        json_file = 'output/' + json_file

    csv_to_json(csv_file, json_file)
