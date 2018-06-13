
Any feature that has been built has a multiple types of testing which includes Functional and Load Testing. All the testing in the framework uses unittest and locust for testing out these changes.

### Functional Validation (Unittest)
Functional testing would involve testing the following scenarios - 
1. GET Request
2. POST Request
3. Success Scenario
4. Failure Scenario

Currently this framework has 6 functional test cases -

Count | Test Case | Description
--- | --- | ---
1 | `test_1_get_api` | **Test GET API with different phone number formats**
2 | `test_2_post_api` | **Test POST API to add a new number and context**
3 | `test_3_api_with_duplicate_entry` | **Test POST API with duplicate entry**
4 | `test_4_api_with_number_context` | **Test GET API with number and context**
5 | `test_5_api_with_wrong_number` | **Test GET API with a wrong number**
6 | `test_6_api_with_invalid_number` | **Test GET API with an invalid number**


### Load Validation (Locust)
Load testing would involve simulataneous requests based on number of request w/ number of users

Currently this framework has 2 load test cases -

Count | Test Case | Description
--- | --- | ---
1 | `get_load_test` | **Load Test GET API.**
2 | `post_load_test` | **Load Test POST API.**















