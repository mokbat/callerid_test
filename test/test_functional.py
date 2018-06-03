#!/usr/bin/env python3

"""
Functional Test Module :
- This module will test the caller id app functionality.
- This module conforms to unittest standards.

Usage :
Run all test cases
- python3 -m unittest <test_module_path>
- python3 -m unittest test_functional.py

Run a specific test case
- python3 <test_module_path> <class_in_module>.<test_name>
- python3 test_functional.py FunctionalValidation.test_1_get_api
"""

# Standard Python Library
from unittest import TestCase, main

# Third Party Python Library
import requests

# Custom Python Library
from logger import Logger

class FunctionalValidation(TestCase):
    """ This class deals with all Functional Test Cases."""
    @classmethod
    def setUpClass(cls):
        """ setUpClass will execute once for this class. Instantiate file logger."""
        # Create a file logger for our test case
        cls.log = Logger().file_logger(__file__)
        cls.file = str(cls.log.root.__dict__["handlers"][1])

    def setUp(self):
        """
        setUp will run before every test case.
        Instantiate URL and Headers for each test case.
        """
        self.log.info("")
        self.log.info("------------------------------------------------------")

        # Default Variables
        self.def_headers = {"Content-Type":"application/json", "charset":"utf-8"}
        self.def_url = "http://localhost:9090/query?number="
        self._url = "http://localhost:9090/query?number"
        self._result = "FAIL"

        self.log.debug("Default Header Value - %s", self.def_headers)
        self.log.debug("Default URL Value - %s", self.def_url)

    def tearDown(self):
        """ tearDown will run after every test case"""
        # Print to log file
        self.log.info("")
        self.log.info("Result - \'%s\'", self._result)
        self.log.info("------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        """ tearDownClass will execute once for this class. """

        # Print the log file location
        cls.log.critical("Log File - %s", cls.file.split(" ")[1])

    def test_1_get_api(self):
        """ Test GET API with different phone number formats """
        for each_number in ["(412)123-1234", "4121231234", "+1-412-123-1234", "+1(412)123-1234"]:

            # Name and Description of the test case
            self.log.info("Sub Test Name - %s with %s", self.id().split(".")[-1], each_number)
            self.log.info("Sub Test Desc - %s", self.shortDescription())

            # Use Subtest to validate different formats of the number
            with self.subTest(each_number):

                self.log.info("")

                # Variables for the API call
                url = self.def_url + each_number

                # Execute the REST API
                response = requests.request(method="GET", url=url, headers=self.def_headers)

                # Declare outcome of the test based on asserts
                self.assertEqual(response.status_code, 200, msg="Sub Test : {} with {} has failed!".format(self.id().split(".")[-1], each_number))


    def test_2_post_api(self):
        """ Test POST API to add a new number and context"""

        # Name and Description of the test case
        self.log.info("Test Name - %s", self.id().split(".")[-1])
        self.log.info("Test Desc - %s", self.shortDescription())

        # Variables for the API call
        url = self.def_url
        data = {"number":"(412)1231234", "context":"Testing"}

        # Execute the REST API
        response = requests.request(method="POST", url=url, headers=self.def_headers, params=data)

        # Declare outcome of the test based on asserts
        self.assertEqual(response.status_code, 200, msg="Test : {} has failed!".format(self.id().split(".")[-1]))

        # Print to log file
        self.log.info("Success with context \'%s\' and number \'%s\'", response.json()["results"][0]["context"], response.json()["results"][0]["number"])

        self._result = "PASS"

    def test_3_api_with_duplicate_entry(self):
        """ Test POST API with duplicate entry """

        # Name and Description of the test case
        self.log.info("Test Name - %s", self.id().split(".")[-1])
        self.log.info("Test Desc - %s", self.shortDescription())

        # Variables for the API call
        url = self._url
        data = {"number": "(412)1231234", "context": "Testing", "name": "Sudhakar"}

        # Execute the REST API
        response = requests.request(method="POST", url=url, headers=self.def_headers, params=data)

        # Declare outcome of the test based on asserts
        self.assertEqual(response.status_code, 406, msg="Test : {} has failed!".format(self.id().split(".")[-1]))

        # Print to log file
        self.log.info("Success with context \'%s\' and number \'%s\'", response.json()["results"][0]["context"], response.json()["results"][0]["number"])

        self._result = "PASS"

    def test_4_api_with_number_context(self):
        """ Test GET API with number and context """

        # Name and Description of the test case
        self.log.info("Test Name - %s", self.id().split(".")[-1])
        self.log.info("Test Desc - %s", self.shortDescription())

        # Variables for the API call
        url = self.def_url
        data = {"number": "(412)1231234", "context": "Testing"}

        # Execute the REST API
        response = requests.request(method="GET", url=url, headers=self.def_headers, params=data)

        # Declare outcome of the test based on asserts
        self.assertEqual(response.status_code, 200, msg="Test : {} has failed!".format(self.id().split(".")[-1]))

        # Print to log
        self.log.info("Success with context \'%s\' and number \'%s\'", response.json()["results"][0]["context"], response.json()["results"][0]["number"])

        self._result = "PASS"

    def test_5_api_with_wrong_number(self):
        """ Test GET API with a wrong number """

        # Name and Description of the test case
        self.log.info("Test Name - %s", self.id().split(".")[-1])
        self.log.info("Test Desc - %s", self.shortDescription())

        # Variables for the API call
        number = "1-(423)961-2222"
        url = self.def_url + number

        # Declare outcome of the test based on asserts
        response = requests.request(method="GET", url=url, headers=self.def_headers)
        self.assertEqual(response.status_code, 404, msg="Test : {} has failed!".format(self.id().split(".")[-1]))

        # Print to log file
        self._result = "PASS"

    def test_6_api_with_invalid_number(self):
        """ Test GET API with an invalid number """

        # Name and Description of the test case
        self.log.info("Test Name - %s", self.id().split(".")[-1])
        self.log.info("Test Desc - %s", self.shortDescription())

        # Variables for the API call
        url = self.def_url
        data = {"number": "ALPHA", "context": "Testing"}

        # Execute the REST API
        response = requests.request(method="GET", url=url, headers=self.def_headers, params=data)

        # Declare outcome of the test based on asserts
        self.assertEqual(response.status_code, 400, msg="Test : {} has failed!".format(self.id().split(".")[-1]))

        # Print to log file
        self.log.info("Failed with context \'%s\' and number \'%s\'", data["context"], data["number"])
        self._result = "PASS"

if __name__ == '__main__':
    main()
