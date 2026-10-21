FROM maven:3.9.6-eclipse-temurin-17

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -m appuser

COPY --chown=appuser:appuser pom.xml .
COPY --chown=appuser:appuser src ./src

USER appuser

RUN mvn clean package

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "target/calculator.jar"]