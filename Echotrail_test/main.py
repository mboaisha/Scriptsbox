import csv
import requests
import time
import uuid
import os
import sys
#import json # TODO: Make a config file to safely store API key and other details.

apikey= str("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
apiurl = "https://api.echotrail.io/v1/private"
headers={'X-Api-key':apikey}
filename = 'parentChild.csv'

# The function to build the JSON output
def jsonBuilder(prelevance, descParent, descChild, parent_proc, child_proc):
    jsonOutput = {
        'id': uuid.uuid4(),
        'meta':
        {
            'guid': uuid.uuid4(),
            'prevalence': round(float(prelevance),2),
            'description': str(descParent) + " " + str(descChild),
            'signature_name': parent_proc +  " spawning "  + child_proc
        },
        'rules': [
        {
            'id': uuid.uuid4(),
            'rules': [
            {
                'id': uuid.uuid4(),
                'field': 'processEvent/parentProcess',
                'value': parent_proc,
                'operator': 'equals'
            },
            {
                'id': uuid.uuid4(),
                'field': 'processEvent/process',
                'value': child_proc,
                'operator': 'equals'
            }],
            'combinator': 'AND'
        }]}

    return str(jsonOutput)

with open(os.path.join(sys.path[0], "parentChild.csv"), "r") as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader)
    for row in datareader:
        time.sleep(2)
        row[0] = row[0].lower() # Parent
        row[1] = row[1].lower() # Child
        request1 = requests.get(apiurl + "/insights/" + row[1] + "/parents/" + row[0], headers=headers) # Parent Relevance
        time.sleep(2)
        request2 = requests.get(apiurl + "/insights/" + row[0] + "/description/", headers=headers) # Parent Description
        time.sleep(2)
        request3 = requests.get(apiurl + "/insights/" + row[1] + "/description/", headers=headers) # Child Description
        prelevance = float(request1.json()[1]) # Sample output: 79.561004
        outputJ = jsonBuilder(prelevance, request2, request3, row[0], row[1])
        print(outputJ)