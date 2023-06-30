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
    # python environment_type_csv_convert.py data\\Dalby_ET1.csv output\\env_types.json

    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <json_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    json_file = sys.argv[2]
    csv_to_json(csv_file, json_file)


