import unittest
import os
import app
import datetime

"""
This test suite tests that the methods defined in app.py work as expected
"""
class TinesTestCase(unittest.TestCase):

    """
    Positive test cases
    """

    # Test findEventParameters method with 1 parameter
    def test_findEventParameters_single_parameter(self):

        #Arrange
        url = "https://www.domain.com?param={{agent.parameter1}}"

        # Act
        matches = app.findEventParameters(url)
        result = []
        for match in matches:  
            result.append(match.group(1))
        
        #Assert
        self.assertEqual(result, ["agent.parameter1"])

    # Test findEventParameters method with 2 parameters
    def test_findEventParameters_two_parameters(self):

        # Arrange
        url = "https://www.domain.com?param={{agent.parameter1}}&param2={{agent.parameter2}}"

        # Act
        matches = app.findEventParameters(url)
        result = []
        for match in matches:  
            result.append(match.group(1))
        
        # Assert
        self.assertEqual(result, ["agent.parameter1","agent.parameter2"])

    # Test findEventParameters method with 3 parameters
    def test_findEventParameters_five_parameters(self):

        # Arrange
        url = "https://www.domain.com?param={{agent.parameter1}}&param2={{agent.parameter2}}&param3={{agent.parameter3}}&param4={{agent.parameter4}}&param5={{agent.parameter5}}"

        # Act
        matches = app.findEventParameters(url)
        result = []
        for match in matches:  
            result.append(match.group(1))
        
        # Assert
        self.assertEqual(result, ["agent.parameter1","agent.parameter2","agent.parameter3","agent.parameter4","agent.parameter5"])

    # Test updateTemplateValue method using a URL thjat contains only 1 parameter values are NOT nested in sub dictionaries, e.g., sunset.results.sunset
    def test_updateTemplateValue_single_parameter_no_nesting_in_variables(self):

        # Arrange
        url = "https://api.sunrise-sunset.org/json?lat={{location.latitude}}"
        httpReqObjects =  {"location":{"latitude": "54.5"}}

        # Act
        matches = app.findEventParameters(url)
        url = app.updateTemplateValue(matches, url, httpReqObjects)

        # Assert
        self.assertEqual(url, "https://api.sunrise-sunset.org/json?lat=54.5")

    # Test updateTemplateValue method using a URL thjat contains only 1 parameter values ARE nested in sub dictionaries, e.g., sunset.results.sunset
    def test_updateTemplateValue_single_parameter_nesting_in_variables(self):

        # Arrange
        message = "Sunset at {{sunset.results.sunset}}."
        httpReqObjects =  {"sunset":{"results": {"sunset": "8:00:00 PM"}}}

        # Act
        matches = app.findEventParameters(message)
        message = app.updateTemplateValue(matches, message, httpReqObjects)

        # Assert
        self.assertEqual(message, "Sunset at 8:00:00 PM.")

    # Test updateTemplateValue method using a URL thjat contains only multiple parameters, values are NOT nested in sub dictionaries, e.g., sunset.results.sunset
    def test_updateTemplateValue_multi_parameter_no_nesting_in_variables(self):

        # Arrange
        url = "https://api.sunrise-sunset.org/json?lat={{location.latitude}}&lng={{location.longitude}}"
        httpReqObjects =  {"location":{"latitude": "54.5", "longitude": "35.4"}}

        # Act
        matches = app.findEventParameters(url)
        url = app.updateTemplateValue(matches, url, httpReqObjects)

        # Assert
        self.assertEqual(url, "https://api.sunrise-sunset.org/json?lat=54.5&lng=35.4")

    # Test updateTemplateValue method using a URL thjat contains multiple parameters, values ARE nested in sub dictionaries, e.g., sunset.results.sunset
    def test_updateTemplateValue_multi_parameter_nesting_in_variables(self):

        # Arrange
        message = "Sunrise at {{sunrise.results.sunrise}}, sunset at {{sunset.results.sunset}}."
        httpReqObjects =  {
            "sunrise":{"results": {"sunrise": "7:00:00 AM"}},
            "sunset":{"results": {"sunset": "8:00:00 PM"}}
            }

        # Act
        matches = app.findEventParameters(message)
        message = app.updateTemplateValue(matches, message, httpReqObjects)

        # Assert
        self.assertEqual(message, "Sunrise at 7:00:00 AM, sunset at 8:00:00 PM.")

    # Test updateTemplateValue method using a a parameters whose variable is not a string
    def test_updateTemplateValue_single_parameter_with_non_string_variable(self):

        # Arrange
        message = "Sunrise at {{sunrise.results.sunrise}}."
        sunrise = datetime.time(7)
        httpReqObjects =  {"sunrise":{"results": {"sunrise": sunrise}}}

        # Act
        matches = app.findEventParameters(message)
        message = app.updateTemplateValue(matches, message, httpReqObjects)

        # Assert
        self.assertEqual(message, "Sunrise at 07:00:00.")


    """
    Negative test cases
    """

    # Test findEventParameters method with an invalid parameter structure
    def test_findEventParameters_invalid_parameter_structure(self):

        # Arrange
        url = "https://www.domain.com?param={agent.parameter1}&param2={{}}&param3={{agent}}"

        # Act
        matches = app.findEventParameters(url)
        
        # Assert
        result = next(matches, None)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()