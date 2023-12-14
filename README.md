# Loan Application System

## Running the App Locally

### Prerequisites
Make sure you have Docker installed on your machine.

### Run Application
To start the application locally, run the following command in the terminal:

```
docker-compose up --build
```

Once the containers are up and running, open http://localhost:3000 in your web browser.

### Run Tests
To execute tests, use the following command:

```
docker-compose exec backend pytest
```

This command runs the tests using Pytest within the backend container.