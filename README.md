## Architecture

This project is designed to set up a **DataLab** environment using **Kubernetes (k3s)** locally, with components like **Minio**, **Hive**, **Spark**, **Jupyter**, and **Postgres** to facilitate data processing, storage, and analytics. This would help me practice spark. Here is a brief overview of each component in the architecture:

- **Kubernetes (k3s)**: A lightweight Kubernetes distribution that simplifies deployment and management of containerized applications, providing a foundation for the services in this project.

- **Minio**: A high-performance, S3-compatible object storage that serves as the primary storage for Delta Lake and other data files in the lab environment.

- **Hive Metastore**: A centralized metadata store that manages the metadata for Spark, enabling efficient data querying and management.

- **Spark (Master and Worker)**: A distributed computing engine for big data processing that runs on Kubernetes. Spark is responsible for processing large datasets and can save data into Delta Lake format.

- **Jupyter**: An interactive notebook environment used to run and experiment with Spark code, perform data analysis, and visualize results in real-time.

- **Postgres**: A relational database management system used for storing relational data, which could serve as an additional data source for the lab.

---

## Setup

Follow these steps to set up your environment:

### 1. Create folder hadoop-libs in the project root
* Download [AWS Java SDK Bundle 1.11.271](https://medium.com/r/?url=https%3A%2F%2Frepo1.maven.org%2Fmaven2%2Fcom%2Famazonaws%2Faws-java-sdk-bundle%2F1.11.271%2Faws-java-sdk-bundle-1.11.271.jar) and [Hadoop AWS 3.1.0](https://medium.com/r/?url=https%3A%2F%2Frepo1.maven.org%2Fmaven2%2Forg%2Fapache%2Fhadoop%2Fhadoop-aws%2F3.1.0%2Fhadoop-aws-3.1.0.jar)
* Place jars in hadoop-libs folder

### 2. Create images for Hive, Spark, and Jupyter
   - Build Docker images for Hive, Spark, and Jupyter locally.
   - Example :
     ```bash
     docker build -t spark-image -f Dockerfile-spark
     docker build -t hive-image -f Dockerfile-hive
     docker build -t jupyter-image -f Dockerfile-jupyter
     ```

### 3. Replace Required Paths and Variables in the Manifest
   - Edit the Kubernetes manifest files to replace the necessary paths and variables, such as image names, volume paths, and environment variables.

### 4. Ingress (Optional)
   - If you'd like to expose the services via an ingress controller, update the URL values in the ingress configuration.
   - Alternatively, you can use **NodePort** for local access.

### 5. Apply the Manifest and Ingress
   - Deploy the services to the cluster using the following command:
     ```bash
     kubectl apply -f <path-to-manifest>.yaml
     kubectl apply -f <path-to-ingress>.yaml
     ```

---

## Current Issues

### Known Error: Delta Table Saving Issue
When saving a DataFrame as a Delta table, you might encounter the following error:
```
spark.saveAsTable(). An error occurred while calling o148.saveAsTable. : java.lang.NoSuchMethodError: void org.apache.hadoop.util.SemaphoredDelegatingExecutor
```
This error is due to a **version mismatch** between Apache Spark and Hadoop libraries. Specifically, certain versions of Spark and Hadoop are incompatible, which causes the method `saveAsTable()` to fail.

#### Workaround:
- **Temporary Solution**: To work around this issue, you can run `spark-submit` directly from inside the container to convert and save tables to Delta format. For example:
  ```bash
  spark-submit <script.py>
  ```
- Interestingly, running the same command inside a container does not produce the version mismatch error, and Delta table operations are executed successfully. I have tried those versions in Jupyter as well, but the error persists there due to the version conflict. I think other jars could be a conflict(Assumption).

---

Further Improvements : 
- Fixing library mismatch error.
- Kubernetes : Storage Management(Using PVC's)
- Kubernetes : ConfigMap to manage variables
- Kubernetes : Secret Management
- Kubernetes : GitOps(Argo vs Flux)
This architecture and setup should provide you with a solid foundation to work with Spark, Minio, Delta Lake, and related technologies in Kubernetes.

