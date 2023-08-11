import os
import csv

#
# A class that handles parsing the CSV data and stores it in memory.
#
class APSimSimulationData:
    _instance = None

    #
    # Singleton.
    #
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APSimSimulationData, cls).__new__(cls)
            cls._instance.data = {}
            cls._instance.load_data()
        return cls._instance

    #
    # Loads the simulation data.
    #
    def load_data(self):
        directory = os.path.join(os.path.dirname(__file__), 'apsim_simulation_data')
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                job_id = os.path.splitext(filename)[0]
                with open(os.path.join(directory, filename), "r") as file:
                    lines = self.parse_csv(file)
                    self.data[job_id] = lines

    #
    # Parses a CSV file.
    #
    def parse_csv(self, file):
        csv_reader = csv.reader(file)
        lines = []
        for index, row in enumerate(csv_reader):
            if index == 0: continue
            simulation_name = row[0].strip()
            lines.append(simulation_name)
        return lines

    #
    # Given a job id, return the simulation data.
    #
    def get_simulation_names(self, job_id):
        return self.data.get(job_id, [])
