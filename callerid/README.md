
![callerid API](http://callapps.studio/images/ic_callerid_logo.png "callerid API")
# callerid API

A standalone service that responds to requests seeking caller id information.
API is built using Spring Boot Web and runs with its embedded tomcat server. 
In addition, we use google's libphonenumber and apache's commons-csv libraries.

By default API lists to port **9090**.  It can be overridden via one of 4 ways.
    
1. change the value in the application.properties file

        $> server.port = 9999
    
2. pass the property through the command line arguments

        $> java -jar build/libs/callerid-api-0.1.0.jar --server.port=9999

3. define server.port system property

        $> java -Dserver.port=9999 -jar build/libs/callerid-api-0.1.0.jar
        
4. Export the OS environment variable SERVER_PORT=8090 

        $> export SERVER_PORT=9999
        $> java -jar build/libs/callerid-api-0.1.0.jar


# API Requirements/Assumptions
- Api returns json response
- Phone numbers are converted to E.164 format using the google's libphonenumber library
- Relative HTTP codes are returned on Success, Error, etc scenarios.
- Port number should be configurable
- May not use an external data store and no persistence need for POST methods
- Seed the services with initial data set CSV file

## Endpoints

### GET /query

Fetches caller id information for the requested phone number.

**Params:**
*number* - the input phone number

**Example:**
GET http://localhost:9090/query?number=(423)961-1337

**Curl Example:**

    curl -H 'Content-Type: application/json; charset=utf-8' http://localhost:9090/query?number="(423)961-1337"

**Response:**

    {"results":[{"name":"Mckelvey Bunker","number":"+14239611337","context":"blah"}]}


Response Code | Description
---           | --- 
 *200*        | Success, Found one or more matching caller id's.
 *400*        | Error, Bad Request.  Either invalid request parameters or invalid phone number format.
 *404*        | Error, phone number not found.

Additional Sample Data for testing all use cases

    curl -H 'Content-Type: application/json; charset=utf-8' http://localhost:9090/query?numbers="(423)961-1337"
    curl -H 'Content-Type: application/json; charset=utf-8' http://localhost:9090/query?number="ALPHA"
    curl -H 'Content-Type: application/json; charset=utf-8' http://localhost:9090/query?number="1-(423)961-2222"

### POST /number

Adds caller Id data to the service.

**POST Header:**
* *Content-Type* - Media Type format, JSON.

**POST Body:**
* *number*  - the number in any string format.  Service will convert it to E.164 format.
* *context* - the context for the phone number
* *name*    - contact name for the phone number

Note: A phone number may be present multiple times, but can only appear once per context. In other words you can think of a <number,context> pair as unique.
The POST body is in JSON string format, to be consistent.

**Curl Example:**

    curl -H "Content-Type: application/json" -d '{"number": "(412)1231234","context": "Testing","name": "Sudhakar"}' http://localhost:9090/number

**Response:**

    {"name":"Sudhakar","number":"+14121231234","context":"Testing"}
    

Response Code | Description
---           | --- 
*200*         | Success: The caller Id data was saved in server.
*400*         | Error, Bad Request.  Either invalid request parameters or invalid phone number format. 
*406*         | Not Acceptable: A record with the combination of phone number and context already exists.

Additional Sample Data for testing all use cases

    #Run any command twice
    curl -H "Content-Type: application/json" -d '{"number": "(412)1231234","context": "Testing","name": "Sudhakar"}' http://localhost:9090/number
    curl -H "Content-Type: application/json" -d '{"number": "(412)1231234","context": "Testing","name": "Sudhakar"}' http://localhost:9090/number
    
    curl -H "Content-Type: application/json" -d '{"number": "(412)1231234","name": "Sudhakar"}' http://localhost:9090/number

## Startup Seed Data

As part of API boot up process, the app reads a CSV file and seeds the initial data to a local Data store.
Initial CSV file is located at /src/main/resource/data/interview-callerid-data.csv.
Original file can be found here: [Link](https://www.dropbox.com/s/0hmkx242o42g924/interview-callerid-data.csv.gz?dl=0)

The file CallerIdService.java has the implementation for the local Data store.
The Current version uses the TreeMap Data Structure as follows:

        private Map<String, Map<String, String>> store = new TreeMap<>();

Benefits of using TreeMap data structure are..
- keep the entries sorted and uses the amount of memory needed to hold its items no extra allocation
- performs well when items are consistently added and removed
- consistent performance of O(log n) for add, remove, contains, etc operations.

Alternatively, this can be replaced by a HashMap or LinkedHashMap (preserves insertion order).
Benefits for this option would be...
- suitable for use cases where its primary used as a Lookup service, instead of read/write. 
- performance varies from  O(1) to O(log n)
- before Java 8 the worst case performance was O(n).  Now when buckets get too large it converts to TreeMap internally.

End of the day, for this solution, I like the Automatic sorting feature and consistent performance for read/write operations.

## Running the application using Docker

1. Download the Repo to your local using Git Clone
2. Build the docker image

       docker build -t callerid .

3. Run the docker container

        docker run -p 9090:8080 callerid
    
4. Run the tests using your browser or Curl command.  See example above for each end points.

## Running the application manually

1. To start the application, go to the project main folder. 

        ./start_app.sh

    The command will kick of Gradle build, executes all Unit Test and Integration Tests and then runs the Spring Boot application using JVM.  Additionally you can override the Port by changing the parameter value directly in this script.
    
    *System Requirements:*
    - Gradle version 4.5 or later
    - JVM version 8 or later

## No testing implemented

# Reference :books:

Here are few reference links if you'd like  to deep dive on these topics.
- [Best practices on handling phone numbers](https://mojolingo.com/blog/2015/best-practices-handling-phone-numbers/)
- [Github Google's libphonenumber Library](https://github.com/googlei18n/libphonenumber)

