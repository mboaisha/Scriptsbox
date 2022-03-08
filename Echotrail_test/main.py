import csv
import requests
import time
import uuid
import os
import sys
import json

apikey= str("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") # API Key goes here
apiurl = "https://api.echotrail.io/v1/private"
headers={'X-Api-key':apikey}
filename = 'parentChild.csv'

# The function to build the JSON output
def jsonBuilder(prevalence, descParent, descChild, parent_proc, child_proc):
    naResults = 0
    try:
        naResults = round(float(prevalence[1]),2)
    except:
        naResults = "No results found"

    jsonOutput = {
        'id': uuid.uuid4(),
        'meta':
        {
            'guid': uuid.uuid4(),
            'prevalence': naResults,
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
        # It seems the API only accepts the process names in lower-case. Lower-case all retrieve process names.
        row[0] = row[0].lower() # Parent
        row[1] = row[1].lower() # Child
        
        # Fetch Parent Prevalance
        request1 = requests.get(apiurl + "/insights/" + row[1] + "/parents/" + row[0], headers=headers) # Parent Prevalence
        request1 = request1.json
        
        # Fetch parent process description
        time.sleep(2)
        request2 = requests.get(apiurl + "/insights/" + row[0] + "/description", headers=headers) # Parent Description
        request2 = request2.json()
        
        # Fetch child process description
        time.sleep(2)
        request3 = requests.get(apiurl + "/insights/" + row[1] + "/description", headers=headers) # Child Description
        request3 = request3.json()

        # Pass to JSON building function.
        outputJ = jsonBuilder(request1, request2['description'], request3['description'], row[0], row[1])
        print(outputJ)