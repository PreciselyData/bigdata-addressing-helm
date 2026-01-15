# Geo Addressing Spark Helm Charts

The helm chart used to run the Geo Addressing capabilities like Geocode, Verify, etc. using Geo Addressing Big Data
solution for Spark on Kubernetes.

This helm chart is based
on [The Geo Addressing SDK for Big Data](https://docs.precisely.com/docs/sftw/hadoop/landingpage/index.html) and is
useful in quickly running the Geo Addressing Application based on Spark.

## Motivation

1. **Simplify Deployment:**
    - Streamline the Geo-Addressing SDK deployment process with Spark.
    - Ensure an effortless deployment experience.
    - Eliminate complexities for users when setting up the SDK.

2. **Seamless Updates:**
    - Guarantee seamless updates for both data and software.
    - Aim for zero downtime during updates, ensuring uninterrupted service.

3. **Hassle-Free Deployments:**
    - Prioritize user-centric deployment experiences.
    - Minimize potential deployment challenges and issues.

4. **Ready-Made Solution:**
    - Develop a plug-and-play solution for immediate use.
    - Minimize the need for extensive setup or configuration.

5. **Language-Barrier Elimination:**
    - Integrate different input or output sources just using configurations.
    - Provide input data in bulk through any supported input source and save it to any supported output source.
    - Eliminate language barriers, enabling broader compatibility.

6. **Dynamic Allocation supported in Deployment for Scalability:**
    - Using Spark's Dynamic Allocation feature, start the application with minimal resource.
    - Scale up the cores and memory by adding more executor as and when data comes which is big in size.
    - Feel free to enhance scalability and performance by modifying Spark based configuration.

> This solution is specifically for users who are looking for Big Data solution with Geo Addressing SDK and
> Kubernetes based deployments.


> [!IMPORTANT]
> 1. Please consider these helm charts as recommendations only. They come with predefined configurations that may not be
     the best fit for your needs. Configurations can be tweaked based on the use case and requirements.
> 2. These charts can be taken as a reference on how one can take advantage of the precisely-data ecosystem and build a
     number of services around the same piece of software, creating a collection of microservices that can scale on a
     need basis.

## Architecture

![geo-addressing-spark_architecture.svg](images/geo-addressing-spark_architecture.svg)

<br>The core of the geo-addressing-spark helm-chart-based solution relies on the Geo-Addressing SDK (GA-SDK). The robust
functionality of GA-SDK forms the backbone of our geo-addressing solution, empowering it to deliver accurate and
efficient
geo-addressing-spark services while maintaining data integrity and usability.

### Capabilities

_Geo Addressing Service with Spark_:

- This application exposes all the relevant configuration to the user to set up
  input/output data sources while deploying the application.
- User can provide their own Spark based configuration to tweak the performance and distribution based on the
  requirements.
- At the time of deployment User can select one from the following geo-addressing capabilities:
    - **_Verify_**: performs address verification and standardization using the specified processing engine.
    - **_Geocode_**: performs forward geocoding using input addresses and returning location data and other information.

## Getting Started

#### 1. Prepare your environment

Install Client tools required for installation. Follow the guides to get the steps for specific cloud
platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-1-prepare-your-environment)

#### 2. Create Kubernetes Cluster

Create or use an existing K8s cluster. Follow the guides to get the steps for specific cloud platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-2-create-the-eks-cluster)

#### 3. Download Geo-Addressing Spark Docker Images

Download docker images and upload to your own container registry. Follow the guides to get the steps for specific cloud
platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-3-download-geo-addressing-spark-docker-images)

#### 4. Create a Persistent Volume

Create or use an existing persistent volume for storing geo-addressing reference-data. Follow the guides to get the
steps for specific cloud platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-4-create-elastic-file-system-efs)

#### 5. Installation of geo-addressing reference data

Download and install the geo-addressing reference data in the persistent volume. Follow the guides to get the steps for
specific cloud platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-5-installation-of-reference-data)

#### 6. Installation of Spark Operator Helm Chart

Deploy the Spark Operator using helm. Follow the guides to get the steps for specific cloud platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-6-installation-of-spark-operator-helm-chart)

#### 7. Deploy the Geo Addressing Spark application

Deploy the geo-addressing-spark application using helm. Follow the guides to get the steps for specific cloud platform:
[EKS](docs/guides/eks/QuickStartEKS.md#step-7-installation-of-geo-addressing-spark-helm-chart)

## Components

- [Understanding Geo-Addressing Helm Chart](charts/component-charts/geo-addressing-spark-on-k8s-generic/README.md#understanding-geo-addressing-helm-charts)
- [Reference Data Structure](docs/ReferenceData.md)
- Pushing Docker Images: [AWS ECR](docs/guides/eks/QuickStartEKS.md#step-3-download-geo-addressing-spark-docker-images)

## Guides

- [Reference Data Installation Helm Chart](charts/component-charts/reference-data-setup-generic/README.md)
- [Quickstart Guide For AWS EKS](docs/guides/eks/QuickStartEKS.md)
- [Usage Guide](docs/guides/UsageGuide.md)
- [Troubleshooting Guide](docs/guides/TroubleShoot.md)

## Setup

- [Kubernetes Setup](charts/component-charts/geo-addressing-spark-on-k8s-generic/README.md)

> NOTE: As of now, geo-addressing helm chart is only supported for AWS EKS.

## Geo-Addressing Spark Helm Version Chart

Following is the helm version chart against geo-addressing-spark PDX docker image version and GA-SDK version.
Product Name: `GEOCODING GEO ADDRESSING BIG DATA DOCKER IMAGE WORLD GLOBAL ALL GLB`

| Docker Image PDX Version & GA-SDK Version | Spark Version | Helm Chart Version |
|-------------------------------------------|---------------|--------------------|
| `1.0.0/2024.6/18th June 2024` & `5.1.682` | 3.5.1         | `0.1.0`            |
| `1.0.0/2026.1/20th Jan 2026` & `11.2.463` | 4.0.1         | `1.0.0`            |

> NOTE: The docker images pushed to the image repository should be tagged with the current helm chart version.

Refer [Downloading Geo-Addressing-Spark Docker Images](docs/guides/eks/QuickStartEKS.md#step-3-download-geo-addressing-spark-docker-images)
for more information.

## Miscellaneous

- [Monitoring the Helm Chart](docs/guides/eks/QuickStartEKS.md#step-7-monitoring-geo-addressing-helm-chart-installation)

## References

- [Releases](https://github.com/PreciselyData/bigdata-addressing-helm/releases)
- [Helm Values](charts/component-charts/geo-addressing-spark-on-k8s-generic/README.md#helm-values)
- [Environment Variables](charts/component-charts/geo-addressing-spark-on-k8s-generic/README.md#environment-variables)

## Links

- [Geo-Addressing Custom Output Fields](https://docs.precisely.com/docs/sftw/ggs/5.0/en/webhelp/GeoAddressingSDKDeveloperGuide/GlobalGeocodingGuide/source/CustomFields/global_custom_output_fields_all_countries.html)
- [Helm Chart Tricks](https://helm.sh/docs/howto/charts_tips_and_tricks/)