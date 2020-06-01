import os
import json
import requests
import re

"""
This is a recursive method used to identify the most nested values in the results of HTTP requests
"""
def checkForRecurssion(httpResult, parameters, index = 0):

    # Parameter will only be a str when passed recursively. When parameter is a str we have our result
    if type(parameters) is str:
        return httpResult[parameters]

    # if len is <= 1 then the result is not nested so no action is needed
    if len(parameters) > 1:

        # Update the dictionary to be the nested dictionary
        httpResult = httpResult[parameters[index]]

        # increment index to access the next parameter and pass this recursively with the nested dictionary
        index=index+1
        return checkForRecurssion(httpResult, parameters[index])

    return httpResult[parameters[index]]

"""
Method used for finding parameters in the URLs and the Message
"""
def findParameters(text):
    # Matches that contain any number of word characters followed by a dot, contained within curly brackets
    pattern = re.compile(r'\{\{([\w.]+)\}\}')
    return pattern.finditer(text)

"""
This method is used to update the template values in the URLs and messages
"""
def updateTemplateValue(match, text):
    # Split the url to identify the agent and the parameters of that agent that are to be accessed
    splitMatch = match.group(1).split(".")

    # Name of the agent, parameter(s) of that agent which need to be used in the url
    agentName, parameters = splitMatch[0], splitMatch[1]

    # Store the nested most value 
    toBeReplaced = checkForRecurssion(httpReqObjects[agentName], splitMatch[1:])

    return text.replace(match.group(0), str(toBeReplaced))


if __name__ == "__main__":

    # Open the tines story
    with open("tines/data/location.json", "r") as json_data:
        story = json.load(json_data)

    # Dictionary storing the results of HTTPRequestAgents
    httpReqObjects = {}
    
    # Loop through the agents in the story file
    for agent in story["agents"]:

        ## If we have a HTTP request, check for parameters in the URL and replace them with the corresponding values
        if agent["type"] == "HTTPRequestAgent":

            # Store url in variable for easier readability
            url = agent["options"]["url"]

            # Find the parameters within the url
            matches = findParameters(url)

            ## If we have a valid match, loop through all matches and replace each match with its corresponding value
            if matches:
                for match in matches:

                    # Replace the template result in the URL with the actual result of the parameter
                    url = updateTemplateValue(match, url)

            # Store the response from the request URL in JSON
            httpReqObjects[agent["name"]] = requests.get(url).json()

        ## If we have a PrintAgent, check for parameters in the message and replace them with the corresponding values
        elif agent["type"] == "PrintAgent":

            # Extract the message from the PrintAgent
            message = agent["options"]["message"]
            
            # Find the parameters within the message
            matches = findParameters(message)
            
            ## If we have a valid match, loop through all matches and replace each match with its corresponding value
            if matches:
                for match in matches:

                    # Replace the template result in the message with the actual result of the parameter
                    message = updateTemplateValue(match, message)

                print(message)
        else:
            print(f"Invalid agent {{agent['name']}} Identified in Tines Story")

