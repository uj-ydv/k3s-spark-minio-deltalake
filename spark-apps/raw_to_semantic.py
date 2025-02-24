from delta.tables import DeltaTable
from pyspark.sql import SparkSession
import argparse
import socket
import logging


# Use try catch block for args parsing and exception handling
try:
    # Setup argument parser to accept three file paths as arguments
    parser = argparse.ArgumentParser(description="Process multiple CSV files to Delta format")
    parser.add_argument("args1", help="The path to the first input CSV file")
    parser.add_argument("args2", help="The name of delta table")
    # Parse arguments
    args = parser.parse_args()
    # Get input paths from command-line arguments
    filename = args.args1
    delta_table = args.args2
    # Check if the arguments are valid and not empty
    if not filename or not delta_table:
        raise ValueError("Both file path and delta table name must be provided.")

except Exception as e:
    print(f"Error: {e}")
    #Exit if the file path and delta table name are not provided
    # Also give example of how to run the script
    if not filename:
        print("------------------------------------------------------------Please provide the path to the input CSV file")
        print("------------------------------------------------------------Example: spark-submit <sample_data.csv> <sample_delta_table>")
        exit(1)


spark = SparkSession.builder \
        .appName("Application-1") \
        .enableHiveSupport() \
        .getOrCreate()

# Define source and target paths
source_bucket = "wba"
sourceSchema = "Raw"
targetSchema = "Semantic"

input_path = f"s3a://{source_bucket}/{sourceSchema}/{filename}"
delta_path = f"s3a://{source_bucket}/{targetSchema}/"
print(f"----------------------------------------------Input path: {input_path}")
print(f"----------------------------------------------Delta path: {delta_path}")


schemas = [db['namespace'] for db in spark.sql("SHOW SCHEMAS").collect()]
if targetSchema.lower() not in schemas:
    print(f"Database {targetSchema} does not exist. Creating one...")
    spark.sql(f"CREATE DATABASE {targetSchema}")

print(f"----------------------------------------------Reading CSV file from {input_path}")
df = spark.read.csv(input_path, header=True, inferSchema=True)
df.show()

print(f"----------------------------------------------Writing to Delta Table {delta_table}")
df.write.format("delta").option("delta.columnMapping.mode", "name")\
    .option("path", f'{delta_path}/{delta_table}')\
    .saveAsTable(f"{targetSchema}.{delta_table}")

print(f"----------------------------------------------Reading Delta Table {delta_table}")
dt = DeltaTable.forName(spark, f"{targetSchema}.{delta_table}")
dt.toDF().show()

# list all tables in the Gold Schema
spark.sql(f"SHOW TABLES IN {targetSchema}").show()