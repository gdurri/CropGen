import logging
import os
import csv
import json
import sys

# Cleanses the string to ensure it only has recognised characters
def cleanse_string(s):
    # Define the set of characters you want to allow in the CSV file
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, _-")
    
    # Filter out any characters not present in the allowed set
    filtered_string = ''.join(filter(allowed_characters.__contains__, s))
    
    return filtered_string

# Parses the CSV and turns it into a JSON array of objects.
def csv_to_json(csv_file, json_file):
    data = {"EnvironmentTypes": []}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader((cleanse_string(line) for line in file))
        for row in reader:
            simulation_name = row['SimulationName']
            season = int(row['Season'])
            environment_type = int(row['EnvType'])

            # Check if the simulation already exists in the JSON
            simulation = next((s for s in data['EnvironmentTypes'] if s['Simulation']['Name'] == simulation_name), None)
            if simulation is None:
                # Create a new simulation entry with the first environment object
                simulation = {
                    "Simulation": {
                        "Name": simulation_name,
                        "Environments": [
                            {
                                "Type": environment_type,
                                "Seasons": [season]
                            }
                        ]
                    }
                }
                data['EnvironmentTypes'].append(simulation)
            else:
                # Check if the environment type already exists for the simulation
                existing_env_type = next((env for env in simulation['Simulation']['Environments'] if env['Type'] == environment_type), None)
                if existing_env_type is None:
                    # Create a new environment object for the environment type
                    environment = {
                        "Type": environment_type,
                        "Seasons": [season]
                    }
                    simulation['Simulation']['Environments'].append(environment)
                else:
                    # Add season to existing environment object
                    existing_env_type['Seasons'].append(season)

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


# Invokes the CSV to JSON process but sorts out paths and filenames etc first.
def process_csv_file(csv_file):
    csv_filename = os.path.basename(csv_file)

    # Create the output directory if it doesn't exist
    output_dir = get_output_directory()
    os.makedirs(output_dir, exist_ok=True)

    # Create the JSON file path by prepending the output directory to the base name of the CSV file
    json_file = os.path.join(output_dir, os.path.splitext(csv_filename)[0] + '.json')

    csv_to_json(csv_file, json_file)

    logging.info(f"Successfully generated {json_file} from {csv_file}")


# Gets the full path of the output directory, assumed to be a sub directory along side the script.
def get_output_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    return output_dir


# Deletes all of the files in the output directory.
def delete_all_files_in_output_directory():
    output_dir = get_output_directory()

    # Delete all files in the output directory
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Sets up the logger
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# Main entry point.
if __name__ == '__main__':
    setup_logging()

    # Example usage:
    # python environment_type_csv_convert.py data\\Dalby_ET1.csv

    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1].lower()

    # Get the directory path of the currently running script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if csv_file == 'all':

        delete_all_files_in_output_directory()

        # Loop through CSV files in the data folder
        data_dir = os.path.join(script_dir, 'data')
        csv_files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]
        for csv_file in csv_files:
            csv_file_path = os.path.join(data_dir, csv_file)
            process_csv_file(csv_file_path)
    else:
        process_csv_file(csv_file)
