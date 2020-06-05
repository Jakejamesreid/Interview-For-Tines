import os
import sys
import json
import requests
import re
import argparse

"""
Method used for finding parameters in the URLs and the Message
"""
def findEventParameters(text):
    # Match pattern for text within double curly braces that has the format word.word which can occur 1 or more times
    pattern = re.compile(r'\{\{((\w+\.)+\w+)\}\}')
    return pattern.finditer(text)
    
"""
This method is used to update the template values in the URLs and messages
"""
def updateTemplateValue(matches, text, httpReqObjects):

    # Loop over each match and replace it with the correct value
    for match in matches:
        # Split the url to identify the agent and the parameters of that agent that are to be accessed
        splitMatch = match.group(1).split(".")

        # Name of the agent, parameter(s) of that agent which need to be used in the url
        agentName, parameters = splitMatch[0], splitMatch[1:]

        if agentName not in httpReqObjects.keys():
            # Value being referenced does not exist
            text = text.replace(match.group(0), "")
        else:
            # Store the nested most value 
            toBeReplaced = checkForRecurssion(httpReqObjects[agentName], parameters)

            # Replace the match with the correct value
            text = text.replace(match.group(0), str(toBeReplaced))

    return text
    
"""
This is a recursive method used to identify the most nested values in the results of HTTP requests
"""
def checkForRecurssion(httpResult, parameters, index = 0):

    # Parameter will only be a str when passed recursively. When parameter is a str we have our result
    if type(parameters) is str:
        return httpResult[parameters]

    # if len is > 1 then the result is nested
    if len(parameters) > 1:

        # Update the dictionary to be the nested dictionary
        httpResult = httpResult[parameters[index]]

        # increment index to access the next parameter and pass this recursively with the nested dictionary
        index=index+1
        return checkForRecurssion(httpResult, parameters[index:])

    return httpResult[parameters[index]]

def main(path):

    # Open the tines story
    try:
        with open(path, "r") as json_data:
            story = json.load(json_data)
    except FileNotFoundError as err:
        raise Exception(err, "The specified file path for the Tines Story is incorrect")
    # Dictionary storing the results of HTTPRequestAgents
    httpReqObjects = {}
    
    # Loop through the agents in the story file
    for agent in story["agents"]:

        ## If we have a HTTP request, check for parameters in the URL and replace them with the corresponding values
        if agent["type"] == "HTTPRequestAgent":

            # Store url in variable for easier readability
            url = agent["options"]["url"]

            # Ensure that the URL is of the correct format
            if type(url) is not str:
                raise TypeError("Provided URL is not of type string")
            # elif "/json" not in url:
            #     raise ValueError(f"URL {url} does not contain a JSON bosy, only requests against URLs that contain JSON bodies are supoorted")

            # Find the event parameters within the URL, if any exist
            eventParameters = findEventParameters(url)

            ## If URL contains parameters, loop through all and replace each match with its corresponding value
            if eventParameters:

                # Replace the template result in the URL with the actual result of the parameter
                url = updateTemplateValue(eventParameters, url, httpReqObjects)
        
            # Make the http request and raise error if request or response is not JSON
            try:
                request = requests.get(url)
                request.raise_for_status()

                if "application/json" not in request.headers.get('content-type'):
                    raise ValueError(f"Response from {url} is not in json format")

            except requests.exceptions.HTTPError as err:
                raise SystemExit(err, f"Invalid URL {url}")  
            except requests.exceptions.RequestException:
                raise Exception(f'Failed to connect to {url}')

            # Store the response from the request URL in JSON
            httpReqObjects[agent["name"]] = request.json()

        ## If we have a PrintAgent, check for parameters in the message and replace them with the corresponding values
        elif agent["type"] == "PrintAgent":

            # Extract the message from the PrintAgent
            message = agent["options"]["message"]
            
            # Ensure that the message is of the correct format
            if type(message) is not str:
                raise TypeError(f"Provided Message {message} is not of type string")

            # Find the event parameters within the message, if any exist
            eventParameters = findEventParameters(message)
            
            ## If we have a valid match, loop through all matches and replace each match with its corresponding value
            if eventParameters:

                # Replace the template result in the message with the actual result of the parameter
                message = updateTemplateValue(eventParameters, message, httpReqObjects)

                print(message)
        else:
            raise ValueError(f"Invalid agent {agent['name']} Identified in Tines Story")


if __name__ == "__main__":

    # Program description
    parser = argparse.ArgumentParser(description='Process a Tines Story.')

    # Add optional --path arguement to pass the path of the Tines Story to be executed, otherwise default path will be used
    parser.add_argument("--path", help="The path to the Tines Story. If no path is entered the program will check for a story call 'tiny_tines_submission.json' at the same location as the 'app.py' file")
    
    # Store command line arguerments
    args = parser.parse_args()

    # If optional path arguement was defined then use that, else use default path
    if args.path:
        main(args.path)
    else:
        main(os.path.dirname(__file__)+"\\tiny-tines-submission.json")