# Reference Data Setup

This Application requires reference data installed in the worker nodes for running geo-addressing
capabilities. This reference data should be deployed
using [persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). This persistent volume is
backed by Network File Storage so that the data is ready to use immediately when the volume is mounted to
the pods.

Follow the aforementioned steps for installation of the reference data in the mounted storage:

## Step 1: Getting Access to Reference Data

To download the reference data,
visit [Precisely Data Portfolio](https://dataguide.precisely.com/) where you can also sign up for a free account and
access files available in your [Precisely Data Experience](https://data.precisely.com/) account.

## Step 2: Creating and Pushing Docker Image

This helm chart requires a `reference-data-extractor-geo-addressing-spark` docker image to be available in Elastic Container Registry (ECR).
Follow the below steps to create and push the docker image to ECR:

```shell
cd ./charts/component-charts/reference-data-setup-generic/docker-images
docker build . -t bigdata-reference-data-extractor:1.0.0
```

For AWS EKS:

```shell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 603016229198.dkr.ecr.us-east-1.amazonaws.com

aws ecr create-repository --repository-name bigdata-reference-data-extractor --image-scanning-configuration scanOnPush=true --region [AWS-REGION]

docker tag bigdata-reference-data-extractor:1.0.0 [AWS-ACCOUNT-ID].dkr.ecr.[AWS-REGION].amazonaws.com/bigdata-reference-data-extractor:1.0.0

docker push [AWS-ACCOUNT-ID].dkr.ecr.[AWS-REGION].amazonaws.com/bigdata-reference-data-extractor:1.0.0
```


## Step 3: Creating Mounted Storage

We already have scripts to create EFS and link to the current EKS cluster. Please follow the steps
mentioned [here](../../../scripts/eks/efs-creator/README.md) to create EFS.

## Step 4: Running the Reference Data Installation Helm Chart

Run the below command for installation of reference data in EFS:

Edit the [values.yaml](../../../values-reference-data-eks.yaml) for providing the information about the reference data to be downloaded.

```shell
helm install addressing-reference-data ./charts/eks/reference-data-setup/ \
-f values-reference-data-eks.yaml \
--debug \
--dependency-update \
--timeout 60m
```

### Helm Values

The following is the summary of some *helm values*
provided by this chart:

> click the `▶` symbol to expand

<details>
<summary><code>image.*</code></summary>

| Parameter          | Description                                              | Default                    |
|--------------------|----------------------------------------------------------|----------------------------|
| `image.repository` | the reference-data-extractor container image repository  | `reference-data-extractor` |
| `image.tag`        | the reference-data-extractor container image version tag | `1.0.0`                    |

<hr>
</details>

<details>
<summary><code>reference-data.*</code></summary>

| Parameter                                 | Description                                                | Default                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|-------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *`reference-data.config.pdxApiKey`        | the apiKey of your PDX account                             | `pdx-api-key`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| *`reference-data.config.pdxSecret`        | the secret key of your PDX account                         | `pdx-api-secret`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `reference-data.config.countries`         | the countries for which you want to install reference data | `{usa,aus,can,gbr,nzl}`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `reference-data.config.dataConfigMap`     | a Map of reference data to be downloaded against countries | `{\"verify-geocode\":{\"usa\":[\"Geocoding MLD US#United States#All USA#Spectrum Platform Data\",\"Geocoding NT Street US#United States#All USA#Spectrum Platform Data\"],\"aus\":[\"Geocoding PSMA Street#Australia#All AUS#Geocoding\",\"Geocoding GNAF Address Point#Australia#All AUS#Geocoding\"]},\"lookup\":{\"usa\":[\"Geocoding MLD US#United States#All USA#Spectrum Platform Data\",\"Geocoding NT Street US#United States#All USA#Spectrum Platform Data\"],\"aus\":[\"Geocoding PSMA Street#Australia#All AUS#Geocoding\",\"Geocoding GNAF Address Point#Australia#All AUS#Geocoding\"]},\"autocomplete\":{\"usa\":[\"Predictive Addressing Points#United States#All USA#Interactive\"],\"aus\":[\"Predictive Addressing Points#Australia#All AUS#Interactive\"]},\"express_data\":{\"usa\":[\"Address Express#United States#All USA#Spectrum Platform Data\",\"POI Express#United States#All USA#Spectrum Platform Data\"],\"aus\":[\"Address Express#Australia#All AUS#Spectrum Platform Data\"]}}` |

<hr>
</details>

### Providing Information of Reference Data to be Downloaded

You can provide the information about the reference data to be downloaded in the format of Map/Dictionary. Below is an
example of default reference data map:

```yaml
  dataConfigMap:
      spark-addressing-data:
        # USA
        - "Geocoding MLD US#United States#All USA#Spectrum Platform Data"
        - "Geocoding NT Street US#United States#All USA#Spectrum Platform Data"
        - "Geocoding Reverse PRECISELYID#United States#All USA#Spectrum Platform Data"
        # Australia
        - "Geocoding PSMA Street#Australia#All AUS#Geocoding",
        - "Geocoding GNAF Address Point#Australia#All AUS#Geocoding"
        # ...
```

<br>The reference data key is in the format:

`[ProductName#Geography#RoasterGranularity#DataFormat]`

e.g. `Geocoding NT Street US#United States#All USA#Spectrum Platform Data`


> NOTE: If you want to download a specific vintage of data always, you can pass the vintage parameter as follows:
>
> [ProductName#Geography#RoasterGranularity#DataFormat#Vintage]
>
> e.g. `Geocoding NT Street US#United States#All USA#Spectrum Platform Data#2023.11`

## Monitoring the Helm Chart

After running the helm chart command, the reference data installation step might take a couple of minutes to download
and extract the reference data in the EFS. You can monitor the progress of the reference data downloads using following
commands:

```shell
kubectl get pods -w
kubectl logs -f -l "app.kubernetes.io/name=addressing-reference-data"
```

[🔗 Return to `Table of Contents` 🔗](../../../README.md#guides)
