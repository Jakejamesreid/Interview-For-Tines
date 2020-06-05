# interview_for_tines
---

## Table of Contents:

* [Project Description](#project-description)
* [Languages Used](#languages-used)
* [How to Run Project Locally](#how-to-run-project-locally)

---

## Project Description
Tiny Tines is a command line program that takes the path to a Tiny Tines Story JSON file as its only command line argument and executes that Story.

A Story file contains a single JSON object. That object has a single key, agents , mapping to an array of Agents. An Agent is a building block of a Story that can be configured to take an action. 

An Agent is described in the Story file by an object with the keys type , name and options. An Agent's name is a string (that must itself be a valid JSON key) and its options are a collection of key/value pairs that depend on the Agent type (a string).

---

## Languages Used

* Python

---

## How to Run Project Locally

To run this project in a local environment, you first need to clone this project from GitHub:

1. Copy the clone URL for the repository by using the "Clone or download" button at the top right of the repo. 
2. In a command line, navigate to the directiory you want to clone the repo to and type the following command:
    ```git clone https://github.com/Jakejamesreid/interview_for_tines.git```
3. For information on how to run the CLI tool, please use the following command.
    ```python app.py --help```
3. Run the program by using the following command. This CLI tool will use the tiny-tines-submission.json file as default.
    ```python app.py```
4. To specify a different Tines Story to the CLI tool, please pass the file path to the path variable as seen below. Ensure that the path starts from the directory that the app.py file is stored in.
    ```python app.py --path "tiny-tines-submission.json"```