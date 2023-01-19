import json
import os

class Config:
  def __init__(self):

    relativePath = '../config/config.json'
    currentScriptDir = os.path.dirname(os.path.realpath(__file__))
    configFileFullPath = os.path.join(currentScriptDir, relativePath)

    with open(configFileFullPath) as jsonConfigFile:
        data = json.load(jsonConfigFile)    
    
    self.jobsBaseUrl = data['jobsBaseUrl']
    self.simGenUrl = data['simGenUrl']