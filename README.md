# Weather-alert

## How to deploy?

0. Make sure you have `aws-cli`, `kubectl` and `helm` installed and accessible from the command line.

1. Make sure you have AWS credentials properly configured. You should fill in the following values in `~/.aws/credentials`:
```
aws_access_key_id=???
aws_secret_access_key=???
aws_session_token=???
```

2. Push your code to the `main` branch so that a Docker image with the newest version of DAGs is deployed to Docker Hub with image name: `makarepio/weather-alert-airflow:latest`.

3. Enter AWS CloudFormation console and create a new stack using a template file `deploy/cfn_template.yaml`.

4. Wait a few minutes before AWS creates a new Kubernetes cluster

5. Configure `kubectl` with the following command:

```bash
aws eks --region us-east-1 update-kubeconfig --name adzd-kubernetes-cluster
```

6. Check if the Kubernetes cluster was created successfully

```bash
kubectl get nodes
```

You should receive an output similar to this, with "Ready" status for the node.

```
NAME                            STATUS   ROLES    AGE   VERSION
ip-172-31-77-183.ec2.internal   Ready    <none>   37m   v1.28.3-eks-e71965b
```

7. Install an EKS add-on for dynamic volume provisioning.

```bash
aws eks create-addon --cluster-name adzd-kubernetes-cluster --addon-name aws-ebs-csi-driver
```

8. Install Apache Airflow Helm chart on the cluster, using the deployed Docker image `makarepio/weather-alert-airflow:latest`.

```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow --create-namespace \
  --set defaultAirflowRepository=makarepio/weather-alert-airflow \
  --set defaultAirflowTag=latest \
  --set images.airflow.pullPolicy=Always \
  --set webserver.defaultUser.password=admin
```

9. In a separate terminal, observe the deployment process with:

```bash
watch kubectl get pods -n airflow
```

10. When all the pods are ready, set up port forwarding to `airflow-webserver` pod.

```bash
kubectl -n airflow port-forward pods/<webserver-pod-name> 8080:8080
```

11. Enter http://localhost:8080. You should be able to access Airflow UI with username `admin` and password `admin`.


## Useful commands

Forcefully shut down an Airflow release:
```bash
kubectl -n airflow delete deployment --all --grace-period=0 --force
kubectl -n airflow delete statefulset --all --grace-period=0 --force
kubectl -n airflow delete pod --all --grace-period=0 --force
kubectl -n airflow delete pvc --all
kubectl -n airflow delete pv --all
```

Enter pod shell:
```bash 
kubectl -n airflow exec -it <pod-name> -- bash
```
