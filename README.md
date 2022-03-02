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

TODO: Add one!

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
- [x] Manually Deploy Application to Kubernetes
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

### Deployment

1. Set up Kubernetes Cluster Control Plane
To start a deployment, you first need a Kubernetes Control Plane (and the master node therein). A Cloudformation template is included in .circleci.

2. Set up Kubernetes Data Plane
The next stup of setting up the Kubernetes cluster is getting nodes running in the data plane. A Cloudformation template is included in .circleci.
After applying this template, you will have a NodeGroup and node(s) for the Data Plane. HOWEVER, these nodes will not yet be part of the cluster!
There is a crucial next step. Please make sure your AMI is an AWS EKS AMI too :)

3. Set up Kubeconfig
To validate the need for the next step, use `aws eks update-kubeconfig` to gain kubectl access to the cluster and list nodes. There won't be any!

4. Update aws-auth with NodeInstanceRole
You must update the aws-auth ConfigMap with the NodeInstanceRole of each worker node! What does that mean?
See: https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html.
The AWS IAM Authenticator on the Control Plane enables access to the cluster. It gets its configuration from the aws-auth ConfigMap.
What we're doing in this step is telling the Authenticator that the nodes' IAM role is kosher to access the cluster.
Update the `aws-auth-cm.yaml` with the output from the DataPlane's NodeInstanceRole (as ARN).
Next, run:
`kubectl apply -f kubernetes/aws-auth-cm.yaml`
To apply the ConfigMap.
You can check its status with `kubectl describe configmap -n kube-system aws-auth`
Wait a little while, and run `kubectl get nodes`, and you should be good to go!

5. Create a Replicaset
We specify a replicaset for our deployment in our kubernetes folder named `clustering-deploy.yaml`. Upon deploying this replicaset, kubernetes
will automatically create two pods with our container running.

6. Create a Load Balancer to expose the deployment
We create a Cluster IP with Kubernetes using our `loadbalancer.yml` manifest. 

`kubectl create -f kubernetes/loadbalancer.yaml`

7. Create Ingress Controls
We need to set up an Ingress service on Kubernetes to ensure external requests can access any webpage. We'll use `ingress.yaml`.

`kubectl apply -f kubernetes/ingress.yaml`

8. Check Deployment!
Let's grab our external IP (DNS name) to check on our deployment. 

`kubectl get service/clustering-service-loadbalancer |  awk {'print $1" " $2 " " $4 " " $5'} | column -t`

If you try connecting to the IP/hostname, you should be good to go!
