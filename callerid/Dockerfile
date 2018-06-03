FROM openjdk:8
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y curl wget zip && \
    wget "https://services.gradle.org/distributions/gradle-4.7-bin.zip" -O /tmp/gradle-4.7-bin.zip && \
    mkdir -p /opt/gradle && \
    unzip -d /opt/gradle /tmp/gradle-4.7-bin.zip && \
    ln -s /opt/gradle/gradle-4.7/bin/gradle /usr/local/bin/gradle
ENV SERVER_PORT=8080
COPY . /app
WORKDIR /app
RUN gradle clean build
CMD ["java", "-jar", "/app/build/libs/callerid-api-0.1.0.jar"]
