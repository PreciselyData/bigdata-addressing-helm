# Installing Geo-Addressing Helm Chart on AWS EKS

## Step 1: Prepare your environment

To deploy the Geo-Addressing application in AWS EKS, install the following client tools:

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [helm3](https://helm.sh/docs/intro/install/)

##### Amazon Elastic Kubernetes Service (EKS)

- [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)

## Step 2: Create the EKS Cluster

You can create the EKS cluster or use existing EKS cluster.

- If you DON'T have EKS cluster, we have provided you with a
  sample [cluster installation script](../../../cluster-sample/eks/create-eks-cluster.yaml). Run the following command from
  parent directory to create the cluster using the script:
    ```shell
    eksctl create cluster -f ./cluster-sample/eks/create-eks-cluster.yaml
    ```

- If you already have an EKS cluster, make sure you have the following add-ons or plugins related to it, installed on the
  cluster:
    ```yaml
    addons:
    - name: vpc-cni
    - name: coredns
    - name: kube-proxy
    - name: aws-efs-csi-driver
    ```
  Run the following command to install addons only:
    ```shell
    aws eks --region [aws-region] update-kubeconfig --name [cluster-name]
    
    eksctl create addon -f ./cluster-sample/eks/create-eks-cluster.yaml
    ```
- Once you create EKS cluster, you can
  apply [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) so that the
  cluster can be scaled vertically as per requirements. We have provided a sample cluster autoscaler script. Please run
  the following command to create cluster autoscaler:
    ```shell
    aws eks --region [aws-region] update-kubeconfig --name [cluster-name]

    kubectl apply -f ./cluster-sample/eks/cluster-auto-scaler.yaml
    ```

**NOTE**: EKS cluster must have the above addons for the ease of installation of Geo-Addressing Helm Chart.

## Step 3: Download Geo-Addressing Spark Docker Images

The geo-addressing helm chart relies on the availability of Docker images for several essential microservices, all of
which are conveniently obtainable from Precisely Data Experience. The required docker images include subscription to the product:

1. Geo Addressing Big Data Docker Image

> [!NOTE]:
> Contact Precisely or visit [Precisely Data Experience](https://data.precisely.com/) for buying subscription to docker image

Once you have purchased a subscription to Precisely Data Experience (PDX), you can directly download Docker images.
Afterward, you can easily load these Docker images into your Docker environment.

We have provided you with the sample scripts to download the docker images
from [Precisely Data Experience](https://data.precisely.com/)
and push it to your Elastic Container Repositories.

(Note: This script requires python, docker and awscli to be installed in your system)

```shell
cd ./scripts/eks/images-to-ecr-uploader
pip install -r requirements.txt
python upload_ecr.py --pdx-api-key [pdx-api-key] --pdx-api-secret [pdx-secret] --aws-access-key [aws-access-key] --aws-secret [aws-secret] --aws-region [aws-region]
```

For more details related to docker images download script, follow the
instructions [here](../../../scripts/eks/images-to-ecr-uploader/README.md)

## Step 4: Create Elastic File System (EFS)

The Geo-Spatial Application requires reference data for geo-addressing capabilities. This reference data should be
deployed using [persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). This persistent
volume is backed by Amazon Elastic File System (EFS) so that the data is ready to use immediately when the volume is
mounted to the pods.

We have provided python script to create EFS and link it to EKS cluster, or directly link existing EFS to the EKS cluster by creating mount targets.

**NOTE: If you already have created mount targets for the EFS to EKS cluster, skip this step.**

- If you DON'T have existing EFS, run the following commands:
  ```shell
  cd ./scripts/eks/efs-creator
  pip install -r requirements.txt
  python ./create_efs.py --cluster-name [eks-cluster-name] --aws-access-key [aws-access-key] --aws-secret [aws-secret] --aws-region [aws-region] --efs-name [precisely-geo-addressing-efs] --security-group-name [precisely-geo-addressing-sg]
  ```

- If you already have EFS, but you want to create mount targets so that EFS can be accessed from the EKS cluster, run the following command:
  ```shell
  cd ./scripts/eks/efs-creator
  pip install -r requirements.txt
  python ./create_efs.py --cluster-name [eks-cluster-name] --existing true --aws-access-key [aws-access-key] --aws-secret [aws-secret-key] --aws-region [aws-region] --file-system-id [file-system-id]
  ```

## Step 5: Installation of Reference Data

The Geo-Addressing Application relies on reference data for performing geo-addressing operations. For more information related to reference data, please refer to [this link](../../ReferenceData.md).


You can make use of a [miscellaneous helm chart for installing reference data](../../../charts/eks/reference-data-setup/README.md), please follow the instructions mentioned in the helm chart or run the below command for installing data in EFS or contact Precisely Sales Team for the reference data installation.
```shell
helm install reference-data ./charts/eks/reference-data-setup/ \
--set "global.region=<aws-region>" \
--set "global.nfs.fileSystemId=<efs-file-system-id>" \
--set "reference-data.dataDownload.image.repository=<e.g. 603016229.dkr.ecr.us-east-1.amazonaws.com/reference-data-extractor>" \
--set "reference-data.dataDownload.image.tag=<e.g. 1.0.0>" \
--set "reference-data.config.pdxApiKey=<>pdx-api-key>" \
--set "reference-data.config.pdxSecret=<pdx-api-secret>" \
--set "reference-data.config.countries={usa}" \
--debug --dependency-update --timeout 60m
```

## Step 6: Installation of Spark Operator Helm Chart

> Note: To deploy Spark Applications smoothly on K8s, we need to install Spark Operator on our EKS cluster.

> Refer [Spark Operator Docs](https://www.kubeflow.org/docs/components/spark-operator/getting-started/) for more information.

> NOTE: Use the same namespace to install geo-addressing-spark helm chart.

```shell
kubectl create namespace addressing-spark

helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm repo update

# Install the operator into the spark-operator namespace and wait for deployments to be ready
helm install spark-operator spark-operator/spark-operator \ 
    --namespace spark-operator \
    --set spark.jobNamespaces={addressing-spark} \
    --create-namespace \
    --wait

```
#### Notes
> If you don't have the helm chart installation, you can also use the following command to install spark-operator
> 
> 
> However, this is not the best practice to install the spark-operator using kubectl apply command.
```shell
kubectl apply -f ./spark-opeator.yml
```
## Step 7: Installation of Geo-Addressing-Spark Helm Chart

> NOTE: For every helm chart version update, make sure you run the [Step 3](#step-3-download-geo-addressing-spark-docker-images) for uploading the docker images with the newest tag.

The simplest way to deploy the geo-addressing-spark application on EKS is by using the provided values.yaml file.

Follow [this user guide](https://help.precisely.com/r/t/1034035260/2025-12-09/Geo-Addressing-SDK-for-Big-Data/pub/Latest/en-US/Geo-Addressing-SDK-for-Big-Data-Guide/Executing-the-Job) which is helpful to understand the parameters to prepare your values.yaml file.

We have provided you a sample [values-geocode-eks.yaml](../../../values-geocode-eks.yaml) file.
You can modify the parameters as per your requirements and run the following command to install the geo-addressing-spark helm chart:

```shell
helm upgrade --install addressing-spark ./charts/eks/geo-addressing-spark-on-k8s \
  -f values-geocode-eks.yaml \
  --namespace addressing-spark \
  --create-namespace \
  --dependency-update \
  --debug
```

However, you can also run the helm install command by providing all the mandatory parameters as shown below:

```shell
helm install addressing-spark ./charts/eks/geo-addressing-spark-on-k8s \
--set "global.nfs.awsRegion=[aws-region]" \ 
--set "global.nfs.fileSystemId=[fileSystemId]" \
--set "global.countries={usa}" \
--set "global.spark.nodeSelector.driver.eks\.amazonaws\.com/nodegroup=[driver-nodegroup]" \
--set "global.spark.nodeSelector.executor.eks\.amazonaws\.com/nodegroup=[executor-nodegroup]" \
--set "geo-addressing-spark.serviceAccount.name=geo-spark-sa" \
--set "geo-addressing-spark.geo-addressing-spark-hook.enabled=true" \
--set "geo-addressing-spark.image.repository=[aws-account-id].dkr.ecr.[aws-region].amazonaws.com/geo-addressing-spark-on-k8s" \
--set "geo-addressing-spark.image.tag=1.0.0" \
--set "geo-addressing-spark.secrets.ACCESS_KEY=[aws-access-key]" \
--set "geo-addressing-spark.secrets.SECRET_KEY=[aws-secret-key]" \
--set "geo-addressing-spark.env.IN_SOURCE=s3" \
--set "geo-addressing-spark.env.OUT_SOURCE=s3" \
--set "geo-addressing-spark.env.file.INPUT_PATH=s3a://[path-to-your-data]" \
--set "geo-addressing-spark.env.file.OUTPUT_PATH=s3a://[path-to-output-folder]" \
--set "geo-addressing-spark.env.READ_OPTIONS=header=true" \
--set "geo-addressing-spark.env.WRITE_OPTIONS=sep=|\,header=true" \
--set "geo-addressing-spark.env.STREAM_CHECKPOINT_DIR=s3a://[path-to-checkpoint-location]" \
--set "geo-addressing-spark.env.INPUT_FIELDS=streetAddress as addressLines[0]\, locationAddress as country" \
--set "geo-addressing-spark.env.OUTPUT_FIELDS=address.formattedStreetAddress as formattedStreetAddress\,address.formattedLocationAddress as formattedLocationAddress\,location.feature.geometry.coordinates.x as x\,location.feature.geometry.coordinates.y as y\,customFields['PB_KEY'] as 'PB_KEY'" \
--namespace addressing-spark \
--create-namespace \
--dependency-update
```

> NOTE: By default, the geo-addressing-spark helm chart runs a hook job, which identifies the latest reference-data vintage
> mount path. You can disable the geo-addressing-spark-hook and manually provide reference data information using `global.manualDataConfig`
>
> Also, for more information, refer to the comments in [values.yaml](../../../charts/component-charts/geo-addressing-spark-on-k8s-generic/values.yaml)


## Step 7: Monitoring Geo-Addressing Helm Chart Installation

Once you run the geo-addressing helm install/upgrade command, it might take a couple of seconds to trigger the deployment. You can run the following command to check the creation of pods. Please wait until all the pods are in running state:
```shell
kubectl get pods -w --namespace addressing-spark
```

When the application is up, you can run the following command to check the spark UI on localhost:4040
```shell
kubectl port-forward addressing-spark-addressing-spark-driver 4040:4040 -n addressing-spark
```
