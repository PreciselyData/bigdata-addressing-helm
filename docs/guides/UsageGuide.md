# Usage Guide

This section offers usage guide tips for installing Geo Addressing Spark on Kubernetes using the Helm chart.

## Supported Sources

### **Blob Storage Source (Amazon S3)**:

If you are using Blob Storage as a data source, ensure the following prerequisites are met

- Configure the environment variables as follows:
    - IN_SOURCE: "s3"
    - OUT_SOURCE: "s3"
- Specify the location of your input data stored in Blob Storage (e.g., Amazon S3):
    - INPUT_PATH: "s3a://path-to-bucket-of-your-input-data"
    - OUTPUT_PATH: "s3a://path-to-bucket-of-your-input-data"
- Choose the appropriate file type for your input data:
    - INPUT_FILE_TYPE: "csv" or "parquet"
    - OUTPUT_FILE_TYPE: "csv" or "parquet"
- To maintain the original file structure when writing to the output directory, include the following parameter:
    - USE_HIERARCHY: "true"

### **Kafka Source**:

If you are using Kafka as a data source, ensure the input data value is in a valid JSON format and following prerequisites are met:

- Configure the environment variables as follows:
    - IN_SOURCE: "kafka"
    - OUT_SOURCE: "kafka"
- Configure the kafka brokers as follows:
    - INPUT_BOOTSTRAP_SERVER: "localhost:9092"
    - OUTPUT_BOOTSTRAP_SERVER: "localhost:9092"
- Configure the topics where you are reading or writing the data:
    - INPUT_TOPIC:
    - OUTPUT_TOPIC:
- Configure the schema of the input data in DDL format:
    - INPUT_SCHEMA:
      Example: If data is {"address": "xxx", "country": "xxx"} then use "address STRING, country STRING" as value of INPUT_SCHEMA

## Supported Operations

Following operations are supported for geo addressing application as of now:

- Geocode
- Verify

## Additional Info

- The spark app is capable of preserving existing columns which can be input columns or extra columns in the file
  available in the input folder.

  > **Limitations**:
  If upcoming files come with more extra columns then those new columns will not be preserved unless the spark app is
  restarted.
  Even if the spark app is restarted, it still won't be able to handle if any existing column is removed.
  Conclusion:
  Schema changes can't be handled at runtime. For new columns: restart the app and For breaking schema: change/remove
  the
  checkpoint directory and then run the job.

  > **Note**:
  After removing checkpoint directory it will reprocess all the available files in the folder so make sure the input
  directory is pointed to the folder containing relevant files or new files only.


- Please refer to
  the [documentation](../../charts/component-charts/geo-addressing-spark-on-k8s-generic/README.md#environment-variables)
  of the helm chart for more info.
