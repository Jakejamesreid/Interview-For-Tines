# Interview For Tines
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

## Tiny Tines by Example
Tiny Tines is a command line program. It takes the path to a JSON file describing a Tiny Tines Story as its only command line argument and then runs that Story.

To understand how it should work, we'll step through how the attached  tiny-tines-sunset.json 
Story should execute with Tiny Tines.

Much like our example full Tines Sunset Story above, the  tiny-tines-sunset.json  Story defines three Agents, two of which are HTTP Request Agents. The first should fetch the longitude and latitude of the location corresponding to the requestor's IP address. The second should use that longitude and latitude to lookup the sunset time at that location. However, then, instead of sending an
email with the sunset time as we did when using Tines proper, we'll simply print it to the console.

(If you're curious, you can compare  sunset.json  and  tiny-tines-sunset.json  to get a sense of how we've stripped things back for Tiny Tines.)

The first Agent defined in  tiny-tines-sunset.json  is:
```
  {
    "type": "HTTPRequestAgent",
    "name": "location",
    "options": {
      "url": "http://free.ipwhois.io/json/"
    }
  }
```

When it runs, it should make a HTTP GET request against http://free.ipwhois.io/json/ and output an Event that corresponds to the JSON response it receives. The output Event should look something like this (we're just showing a small selection of the fields in this document for clarity):
```
{
  "location": {
    // ...
    "country": "Ireland",
    // ...
    "city": "Dublin",
    "latitude": "53.3165322",
    "longitude": "-6.3425318",
    // ...
  }
}
```

Note that this output Event is just an internal construct. It isn't, e.g., printed to the console. It's just passed to the second Agent as that Agent's input Event. So the second Agent receives that Event as its input and is defined as follows:
```
  {
    "type": "HTTPRequestAgent",
    "name": "sunset",
    "options": {
      "url": "https://api.sunrise-sunset.org/json?lat={{location.latitude}}&lng={{location.longitude}}"
    }
  }
```

When it runs, it should interpolate the correct values into the URL from its input Event, so that the URL it requests looks something like  https://api.sunrise-sunset.org/json?lat=53.3338&lng=-6.2488 . Its output Event should then look something like this:
```
{
  "location": {
    // ...
    "country": "Ireland",
    // ...
    "city": "Dublin",
    // ...
  },
  "sunset": {
    "results": {
      "sunrise": "5:04:59 AM",
      "sunset": "7:41:16 PM",
      // ...
    },
    "status": "OK"
  }
}
```

The final Agent, in turn, receives that Event as its input. It is defined as follows:
```
  {
    "type": "PrintAgent",
    "name": "print",
    "options": {
      "message": "Sunset in {{location.city}}, {{location.country}} is at {{sunset.results.sunset}}."
    }
  }
```

When it runs, it should interpolate the correct values into its message so that it prints the following to STDOUT:
```
Sunset in Dublin, Ireland is at 7:41:16 PM.
```

## The Excercise

The exercise is to implement Tiny Tines in the programming language that you're most comfortable in. When you're done, you should be able to run your program roughly like this (using Ruby as an example):
````
$ ruby tiny-tines.rb tiny-tines-sunset.json
Sunset in Dublin, Ireland is at 7:41:16 PM.
````

Your program should be able to run any Tiny Tines Story JSON file and not just  tiny-tinessunset.json. You can try the other example story that's attached, tiny-tines-today.json, which has a couple more Agents to test things out. It should run something like this:
``
$ ruby tiny-tines.rb tiny-tines-today.json 
Current time:
    2020-05-05T12:20:23.377146+01:00
Fact for today:
    May 5th is the day in 1762 that Russia and Prussia sign the Treaty of St. Petersburg.
``

You should write your code as if you're going to commit it to a production code base (including tests
that use an automated testing framework). Hopefully it should take just a few hours to complete the exercise. There is no time limit for getting back to us.

Your implementation must:
* include tests using an automated testing framework
* run any valid Tiny Tines Story JSON file as described by the specification below
Don't hardcode it so that it will only solve the attached tiny-tines-sunset.json and tiny-tines-today.json files.

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
