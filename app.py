import os
import json
import requests
import re

class Agent:
    def __init__(self, name, url, urlParameters, result):
        self.name = name
        self.url = url
        self.urlParameters = urlParameters
        self.result = result

def checkDict(checkRecurssion, parameters, index = 0):
    if type(parameters) is str:
        return checkRecurssion[parameters]

    if len(parameters) > 1:
        if type(checkRecurssion.result[parameters[index]]) is dict:
            if index is not len(parameters):
                checkRecurssion = checkRecurssion.result[parameters[index]]
                index=index+1
                return checkDict(checkRecurssion, parameters[index])
            else: checkRecurssion.result[parameters]

    else:
        return checkRecurssion.result[parameters[index]]

def findParameters(text):
    pattern = re.compile(r'\{\{([\w.]+)\}\}')
    return pattern.finditer(text)

if __name__ == "__main__":

    # Open the tines story
    with open("tines/data/location.json", "r") as json_data:
        story = json.load(json_data)

    # Stores the parameters contained within the request URL
    urlParameters = []
    messageParameters = []

    # Dictionary to store the results of each HTTP Agent
    httpAgent= {}

    # Objects
    objects = {}
    
    # Loop through the agents in the story file
    for agent in story["agents"]:
        agentName = agent["name"]

        ## If we have a HTTP request, check for parameters in the URL and store them in urlParameters
        if agent["type"] == "HTTPRequestAgent":

            url = agent["options"]["url"]

            # Create result dictionary for each agent
            objects[agent["name"]] = Agent(agentName, url, [], {})

            # Find matches that contain any number of word characters followed by a dot, contained within curly brackets
            matches = findParameters(url)

            # If we have a valid match, loop through all matches and store that part of the regex pattern contained within the parenthesis
            if matches:
                for count, match in enumerate(matches):

                    # Split the url to identify the agent and the parameters of that agent that are to be accessed
                    splitMatch = match.group(1).split(".")

                    # Name of the agent, parameter(s) of that agent which need to be used in the url
                    agentName = splitMatch[0]

                    # Replace the template result in the URL with the actual result
                    url = url.replace(match.group(0), objects[agentName].result[splitMatch[1]])
                    
                # Store the update URL
                objects[agent["name"]].url = url

            # Store the response from the request URL in JSON
            objects[agent["name"]].result = requests.get(url).json()

            
        

        elif agent["type"] == "PrintAgent":

            # Extract the message
            message = agent["options"]["message"]
            
            # Find matches that contain any number of word characters followed by a dot, contained within curly brackets
            matches = findParameters(message)
            
            # If we have a valid match, loop through all matches and store that part of the regex pattern contained within the parenthesis
            if matches:
                for count, match in enumerate(matches):
                    messageParameters.append(match.group(1))
                    splitRes = match.group(1).split(".")
                    agentName = splitRes[0]

                    toBeReplaced = ""   
                    toBeReplaced = checkDict(objects[agentName], splitRes[1:])

                    message = message.replace(match.group(0), toBeReplaced)
                print(message)
        else:
            print("Please enter a valid agent")

