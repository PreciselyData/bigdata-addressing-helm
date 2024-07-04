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
cd ./scripts/images-to-ecr-uploader
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
--set "global.pdxApiKey=[your-pdx-key]" \
--set "global.pdxSecret=[your-pdx-secret]" \
--set "global.efs.fileSystemId=[fileSystemId]" \
--set "dataDownload.image.repository=[reference-data-image-repository]" \
--dependency-update --timeout 60m
```

## Step 6: Installation of Spark Operator Helm Chart

> Note: To deploy Spark Applications smoothly on K8s, we need to install Spark Operator on our EKS cluster.

```shell
aws ecr get-login-password --region [aws-region] | helm registry login --username AWS --password-stdin [aws-ecr-account-id].dkr.ecr.[aws-region].amazonaws.com

helm install spark-operator \
  oci://[aws-ecr-account-id].dkr.ecr.[aws-region].amazonaws.com/spark-operator \
  --set emrContainers.awsRegion=[aws-region] \
  --set webhook.enable=true \
  --set serviceAccounts.sparkoperator.name=geo-spark-sa \
  --version [version-tag-for-spark-operator] \
  --namespace geo-spark \
  --create-namespace

```
#### Notes
> 1. You can find AWS ECR account id by region [on this link](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/docker-custom-images-tag.html#docker-custom-images-ECR)
> 2. More details regarding Spark Operator installation can be found [on this link](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/spark-operator-gs.html#spark-operator-install)

## Step 7: Installation of Geo-Addressing-Spark Helm Chart

> NOTE: For every helm chart version update, make sure you run the [Step 3](#step-3-download-geo-addressing-spark-docker-images) for uploading the docker images with the newest tag.

To install the geo-addressing-spark helm chart, use the following command:

```shell
helm install geo-addressing-spark ./charts/eks/geo-addressing-spark-on-k8s \
--set "global.nfs.awsRegion=[aws-region]" \ 
--set "global.nfs.fileSystemId=[fileSystemId]" \
--set "global.countries={usa,can,aus,nzl}" \
--set "global.spark.nodeSelector.driver.eks\.amazonaws\.com/nodegroup=[driver-nodegroup]" \
--set "global.spark.nodeSelector.executor.eks\.amazonaws\.com/nodegroup=[executor-nodegroup]" \
--set "geo-addressing-spark.serviceAccount.name=geo-spark-sa" \
--set "geo-addressing-spark.geo-addressing-spark-hook.enabled=false" \
--set "geo-addressing-spark.image.repository=[aws-account-id].dkr.ecr.[aws-region].amazonaws.com/geo-addressing-spark-on-k8s" \
--set "geo-addressing-spark.image.tag=0.1.0" \
--set "geo-addressing-spark.secrets.ACCESS_KEY=[aws-access-key]" \
--set "geo-addressing-spark.secrets.SECRET_KEY=[aws-secret-key]" \
--set "geo-addressing-spark.env.IN_SOURCE=s3" \
--set "geo-addressing-spark.env.OUT_SOURCE=s3" \
--set "geo-addressing-spark.env.file.INPUT_PATH=s3a://[path-to-your-data]" \
--set "geo-addressing-spark.env.file.OUTPUT_PATH=s3a://[path-to-output-folder]" \
--set "geo-addressing-spark.env.ADDITIONAL_OPTIONS_READ=header=true" \
--set "geo-addressing-spark.env.ADDITIONAL_OPTIONS_WRITE=checkpointLocation=s3a://[path-to-checkpoint-location],sep=|\,header=true" \
--set "geo-addressing-spark.env.INPUT_FIELDS=streetAddress as addressLines[0]\, locationAddress as country" \
--namespace geo-spark \
--create-namespace \
--dependency-update
```

> NOTE: By default, the geo-addressing-spark helm chart runs a hook job, which identifies the latest reference-data vintage
> mount path. You can disable the geo-addressing-spark-hook in the subsequent installations by using `geo-addressing-spark-hook.enabled`
>
> Also, for more information, refer to the comments in [values.yaml](../../../charts/component-charts/geo-addressing-spark-on-k8s-generic/values.yaml)
#### Mandatory Parameters

* ``global.awsRegion``: AWS Region
* ``global.nfs.fileSystemId``: The ID of the EFS mounted with the cluster and contains the reference data.
* ``global.nodeSelector``: The node selector to run the geo-addressing solutions on nodes of the cluster. Should be a amd64 based Node group.
* ``global.countries``: Required countries for Geo-Addressing (e.g. ``--set "global.countries={usa,deu,gbr}"``).
  Provide a comma separated list to enable a particular set of countries from: `{usa,gbr,deu,aus,fra,can,mex,bra,arg,rus,ind,sgp,nzl,jpn,world}`
* ``geo-addressing-spark.image.repository``: The ECR image repository for the geo-addressing-spark image
* ``geo-addressing-spark.image.tag``: The ECR image tag for the geo-addressing-spark image
* ``geo-addressing-spark.serviceAccount.name`` should be same as the one provided in the Spark Operator helm command.
* ``geo-addressing-spark.env.IN_SOURCE`` Choose what should be your source of input data. [local,s3,Kafka]
* ``geo-addressing-spark.env.OUT_SOURCE`` Choose what should be your destination for output data. [local,s3,Kafka]

For more information on helm values, follow [this link](../../../charts/component-charts/geo-addressing-spark-on-k8s-generic/README.md#helm-values).

## Step 7: Monitoring Geo-Addressing Helm Chart Installation

Once you run the geo-addressing helm install/upgrade command, it might take a couple of seconds to trigger the deployment. You can run the following command to check the creation of pods. Please wait until all the pods are in running state:
```shell
kubectl get pods -w --namespace geo-spark
```

When the application is up, you can run the following command to check the spark UI on localhost:4040
```shell
kubectl port-forward geo-addressing-spark-geo-spark-driver 4040:4040 -n geo-spark
```
