# Troubleshooting

This section offers troubleshooting tips related to the installation of Geo Addressing Spark deployment on Kubernetes
using Helm chart.

## Common Issues

#### 1. Spark Driver Pod Visibility Issues:

What should I do if the Spark driver pod is not visible after running the Helm chart?
Ensure that you have completed the prerequisites:

- The Spark Operator must be installed beforehand, as specified in the Quick Start Guides.
- Use the same Service Account name that was used during Spark Operator installation.
- Verify proper installation of reference data. Refer to the Helm chart for instructions on installing the
  reference data.
- Check the logs of the SparkOperator pod for insights into the issue.

#### 2. Errors at Spark Driver or Executor Pod:

What should I do if there are failures at the driver or executor pods?

- Review node selectors configuration.
- Verify the ECR image repository settings.
- Ensure details related to NFS such as fileSystemId and region are correctly configured.
- Check required environment variables such as paths to input and output files, in-source and out-source
  configurations, etc.
