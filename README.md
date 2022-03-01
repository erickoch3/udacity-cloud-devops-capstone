# Chinese News Clustering

A DevOps project to demonstrate auto-deploying a microservice application using Docker via blue-green deployment.

## Design

This project consists of two phases reflecting simple and full scope.

1. Simple Scope

Within the simple scope, we upload a database of Chinese news files scraped from the internet.
A call to the url, `http://[url]/get_topics`, will return clusters of Chinese news articles from the database
using KMeans clustering from sklearn.

Our focus is less on the application and more on our deployment process.
Once you set up CI/CD, it's much easier to make and test changes to eventually reach the full scope!

#### Pipeline
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-blue-green.html

The blue-green deployment pipeline will consist of the following:
* Build
    - Linting
* Test
    - Run simple unit tests
* Scan
    - Analyze for security risks.
* Deploy Infrastructure
    - Push Container: Upload Docker image to image repository.
    - Deploy Cluster: Use CloudFormation to deploy Kubernetes cluster and nodegroups.
    - Deploy Container: Use CloudFormation to deploy a new container in a Kubernetes cluster.
* Smoke Test
    - Use Locust to test the container in the Kubernetes cluster.
* Cloudfront Update
    - If it passes, update Cloudfront to point to the new container.

2. Full Scope

The above enables us to continuously roll out updates to our app.
However, to really take advantage of the possibilities of our app, we would set up 
a daily Lambda service (on a timer) that scrapes specified sites and updates a database maintained
via RDS. The docker containers would read the database from RDS and use that
database to output clusters.

### Overarching Diagram

# TODO: Add one!

### Planning - Key Actions

#### Simple Scope
- [x] Design and Build Basic App (Clusterinig)
- [x] Dockerize Application
- [x] Create CircleCI Pipeline
- [x] Add Simple Unit Test and Testing Stage
- [x] Add Security Scanning
- [x] Build Kubernetes Control Plane with Cloudformation
- [x] Build Kubernetes Data Plane wiith Cloudformation
- [x] Push Docker Application to Hub
- [ ] Manually Deploy Application to Kubernetes
- [ ] Automate Push and Deploy in CircleCI
- [ ] Add Smoke Testing
- [ ] Add Rollback Steps for Failure
- [ ] Implement Blue-Green Deployment (Shift Traffic)
- [ ] Add Cleanup Stage
- 

#### Full Scope
- [ ] Add Database for News Articles
- [ ] Add Storage for Model
- [ ] Implement Date Tagging of Articles
- [ ] Add Lambda Service to Scrape Daily for new Articles
- [ ] Point Web App to RDS
- [ ] Add Clustering of Daily Articles
- [ ] Improve UI

### Dependencies
For this project, set up a virtual environment for consistency:

```bash
python3 -m venv ~/.devops
source ~/.devops/bin/activate
```

Install those dependencies from our requirements.txt file automatically:
```bash
make install
```

You additionally will need Docker, Hadolint, Kubernetes, minikube, AWS, and CircleCI to fully test and harness this application.

### Linting

We use Hadolint for our Dockerfile and pylint for the source code. These are run automatically through the Makefile.

```bash
make lint
```