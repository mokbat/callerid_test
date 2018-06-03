#!/usr/bin/env bash
gradle clean build
java -jar build/libs/callerid-api-0.1.0.jar --server.port=9090