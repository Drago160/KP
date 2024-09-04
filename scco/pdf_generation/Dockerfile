FROM gradle:8.7-jdk17 as build
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle build

FROM openjdk:19
WORKDIR /app
COPY --from=build /home/gradle/src/build/libs/src-1.0-SNAPSHOT.jar /app/app.jar
CMD ["java", "-jar", "/app/app.jar"]
