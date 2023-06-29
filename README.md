### app
This repository contains the web application of our project.

### Prerequisites

You need to have Docker, Docker Compose, and Kubernetes (if deploying on k8s) installed on your local machine.

### Running Locally

To run the application (first clone this repository and enter the root folder) locally using Docker, use this command:
```
docker build -t <TAG_NAME> .
```

You can choose an option tagname for the docker build. Now enter the following command (with the same tagname used earlier):
```
docker run -it --rm -p 8081:5000 <TAG_NAME>
```

### Website Url
```
localhost:8081
```
