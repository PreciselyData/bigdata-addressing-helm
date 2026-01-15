# Geo Addressing Spark Helm Chart

Built upon the [architecture](../../../README.md#architecture), the geo-addressing-spark helm chart offers flexibility to
users, allowing them to configure and set up infrastructure according to their
specific requirements.

For example, if a user wishes to establish 'verify' and 'geocode' functionalities
for the 'USA,' 'CAN,' 'GBR,' and 'DEU' countries exclusively, they can provide the necessary configurations during the
Helm chart installation to deploy this specific type of infrastructure.

## Getting Started

To get started with installation of helm chart, follow:
<br><br>For Amazon EKS: [Quick Start Guide for EKS](../../../docs/guides/eks/QuickStartEKS.md)

## Understanding Geo Addressing Helm charts

The geo-addressing-spark helm chart compromises of following components:

- Environment Specific Parent Helm Chart
    - The environment specific parent chart is responsible for configurations related to specific cloud platform like
      network file storages, regions, etc.

- Component Chart
    - The geo-addressing-spark generic component chart is responsible for the deployment of `geo-addressing-spark`.
    - Additionally, it contains all the necessary helm components responsible for deploying geo-addressing application.

Feel free to modify these helm charts and update it based on your needs.

## Helm Values

The `geo-addressing-spark` helm chart follows [Go template language](https://pkg.go.dev/text/template) which is driven
by [values.yaml](values.yaml) file. The following is the summary of some *helm values*
provided by this chart:

> click the `▶` symbol to expand

<details>
<summary><code>image.*</code></summary>

| Parameter          | Description                                          | Default |
|--------------------|------------------------------------------------------|---------|
| `image.repository` | the geo-addressing-spark container image repository  | ``      |
| `image.tag`        | the geo-addressing-spark container image version tag | `1.0.0` |

<hr>
</details>

<details>
<summary><code>global.*</code></summary>

| Parameter                                         | Description                                                                                                                                                                                                                        | Default                        |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|
| `global.countries`                                | this parameter enables the provided country for an addressing functionality. A comma separated value can be provided to enable a particular set of countries from: `usa,gbr,deu,aus,fra,can,mex,bra,arg,rus,ind,sgp,nzl,jpn,world` | `{usa,gbr,aus,nzl,can}`        |
| `global.nfs.addressingBasePath`                   | the base path of the folder where verify-geocode data is present                                                                                                                                                                   | `verify-geocode`               |

<hr>
</details>

<details>
<summary><code>spark.*</code></summary>

| Parameter                  | Description                                                                                                                                                    | Default    |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `spark.version`            | Spark Version is linked with the docker image that is being provided.                                                                                          | `3.5.1`    |
| `spark.app_name`           | Provide here the name of Spark Application.                                                                                                                    | `localApp` |
| `spark.log_level`          | Change the logging level of Spark libraries. [DEBUG,INFO,WARN,ERROR]                                                                                           | `WARN`     |
| `spark.dynamic_allocation` | flag to enable or disable dynamic allocation in spark.                                                                                                         | `true`     |
| `spark.initial_executors`  | define here the number of executors to spin up when application starts. This flag will only take effect if dynamic allocation is enabled.                      | `1`        |
| `spark.min_executors`      | set the number of executors which will always be up whether there is data to process or not. This flag will only take effect if dynamic allocation is enabled. | `1`        |
| `spark.max_executors`      | set the maximum number to which executors can be horizontally scaled up. This flag will only take effect if dynamic allocation is enabled.                     | `true`     |
| `spark.driver.cores`       | number of cores to be used by the driver pod.                                                                                                                  | `1`        |
| `spark.driver.memory`      | define here how much memory to allocate to the driver pod.                                                                                                     | `2g`       |
| `spark.executor.cores`     | number of cores to be used by each executor pod.                                                                                                               | `7`        |
| `spark.executor.memory`    | define here how much memory to allocate to each executor pod.                                                                                                  | `16g`      |
| `spark.conf`               | set the Spark config here to optimize Spark runtime.                                                                                                           |            |

<hr>
</details>

<details>
<summary><code>secrets.*</code></summary>

| Parameter            | Description                                                                                                            | Default |
|----------------------|------------------------------------------------------------------------------------------------------------------------|---------|
| `secrets.ACCESS_KEY` | If you are using AWS services then set the AWS access key with this flag. This will be used as a secret from K8s side. | ``      |
| `secrets.SECRET_KEY` | If you are using AWS services then set the AWS secret key with this flag. This will be used as a secret from K8s side. | ``      |

<hr>
</details>

<details>
<summary><code>geo-addressing-spark-hook.*</code></summary>

| Parameter                           | Description                                                                                                                                                                                                   | Default |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `geo-addressing-spark-hook.enabled` | flag to enable or disable the hook jobs for identifying the latest vintage. If you have already installed helm chart once and there is no data update, you can set it to `false` in subsequent installations. | `true`  |

<hr>
</details>

<details>
<summary><code>serviceAccount.*</code></summary>

| Parameter             | Description                                                                 | Default |
|-----------------------|-----------------------------------------------------------------------------|---------|
| `serviceAccount.name` | Name of the service account which was used with Spark Operator installation | `spark` |

<hr>
</details>

## Environment Variables

> click the `▶` symbol to expand.

NOTE: `*` indicates that we recommend not to modify those values during installation.

<details>
<summary><code>geo-addressing-spark</code></summary>

Refer to [this file](templates/spark-deployment.yml) for overriding the environment variables
service.

| Parameter                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Default   |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| `env.IN_SOURCE`             | To define what is the input source for the job. Supported: [local,s3,kafka]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `s3`      |
| `env.OUT_SOURCE`            | To define where to store the result. Supported: [local,s3,kafka]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `s3`      |
| `env.READ_OPTIONS`          | To add spark options when reading from source. Ex: "key1=value1,key2=value2". These options would be format/fileType specific. If IN_SOURCE is file system and file type is CSV then this [document](https://spark.apache.org/docs/3.5.1/sql-data-sources-csv.html) can be referred.                                                                                                                                                                                                                                                                          | ``        |
| `env.WRITE_OPTIONS`         | To add spark options when writing to source. Ex: "key1=value1,key2=value2". These options would be format/fileType specific. If OUT_SOURCE is file system and file type is CSV then this [document](https://spark.apache.org/docs/3.5.1/sql-data-sources-csv.html) can be referred.                                                                                                                                                                                                                                                                           | ``        |
| `env.STREAM_CHECKPOINT_DIR` | Spark needs a checkpoint directory to keep streaming metadata. Preferably use a persistent object storage like S3 directory for it. If not provided then when redeploying the job, it will not resume from last point but restart from beginning.                                                                                                                                                                                                                                                                                                             | ``        |
| `env.OPERATION`             | Can be Geocode or Verify.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `geocode` |
| `env.RETAIN_COLUMNS`        | To retain the source data columns in the output files.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `true`    |
| `env.ERROR_FIELD`           | Column name for errors to record per data.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `error`   |
| `env.JSON_RESPONSE`         | If provided then under this column full result will come as a json string.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | ``        |
| `env.INPUT_FIELDS`          | Mapping of input column to address data. Ex: "InputCol1 as addressLines[0],InputCol2 as country". Find [here](https://docs.precisely.com/docs/sftw/hadoop/landingpage/docs/geocoding/webhelp/Geocoding/source/geocoding/addressing/addressing_input_fields.html) all the columns which can be mapped for address                                                                                                                                                                                                                                              | ``        |
| `env.OUTPUT_FIELDS`         | The columns which are specifically required in output data. Ex: "customFields['PB_KEY'] as 'PB_KEY',address.formattedStreetAddress as formatted". Refer to the documentation [here](https://docs.precisely.com/docs/sftw/hadoop/landingpage/docs/geocoding/webhelp/Geocoding/source/geocoding/addressing/addressing_output_fields.html). Find all custom output fields [here](https://docs.precisely.com/docs/sftw/ggs/5.0/en/webhelp/GeoAddressingSDKDeveloperGuide/GlobalGeocodingGuide/source/CustomFields/global_custom_output_fields_all_countries.html) | ``        |
| `env.REPARTITION_NUM`       | Provide a valid number if input data should be repartition to that number before execution                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | ``        |
| `env.COALESCE_NUM`          | Provide a valid number to coalesce output data to that number of partitions before writing. Use negative to do full shuffle instead of coalesce.                                                                                                                                                                                                                                                                                                                                                                                                              | ``        |

<hr>
</details>
<details>
<summary><code>kafka specific</code></summary>

Refer to [this file](templates/spark-deployment.yml) for overriding the Kafka specific environment variables
service.

| Parameter                           | Description                                                                                                                                                                 | Default |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `env.kafka.INPUT_TOPIC`             | The topic to read data from. Required IN_SOURCE=kafka                                                                                                                       | ``      |
| `env.kafka.INPUT_BOOTSTRAP_SERVER`  | URI of Kafka brokers to read data from. Required IN_SOURCE=kafka                                                                                                            | ``      |
| `env.kafka.INPUT_SCHEMA`            | Schema of Input Data in DDL format. Ex: if data is {"address": "xxx", "country": "xxx"} the schema should be **"address STRING, country STRING"**. Required IN_SOURCE=kafka | ``      |
| `env.kafka.OUTPUT_TOPIC`            | The topic to write output data to. Required OUT_SOURCE=kafka                                                                                                                | ``      |
| `env.kafka.OUTPUT_BOOTSTRAP_SERVER` | URI of Kafka brokers to write data to. Required OUT_SOURCE=kafka                                                                                                            | ``      |
<hr>
</details>
<details>
<summary><code>file system specific</code></summary>

Refer to [this file](templates/spark-deployment.yml) for overriding the File System specific environment variables
service.

| Parameter                   | Description                                                                                                            | Default |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------|---------|
| `env.file.INPUT_FILE_TYPE`  | Define type of input file. Can be csv,parquet. Required IN_SOURCE: file system i.e. [local, s3]                        | ``      |
| `env.file.OUTPUT_FILE_TYPE` | If the OUT_SOURCE is a file system then define type of file. Can be text,csv,parquet etc.                              | ``      |
| `env.file.INPUT_PATH`       | Path to the file. Required IN_SOURCE: file system i.e. [local, s3]                                                     |         |
| `env.file.OUTPUT_PATH`      | Path for the output file. Required OUT_SOURCE: file system i.e. [local, s3]                                            | ``      |
| `env.file.USE_HIERARCHY`    | To save the output files within the folder having same name as input file. IN/OUT_SOURCE: file system i.e. [local, s3] | `false` |

<hr>
</details>

You can adjust the values in [values.yaml](values.yaml), or you can set these parameters in the helm command itself
during installation/up-gradation.

[🔗 Return to `Table of Contents` 🔗](../../../README.md#components)
