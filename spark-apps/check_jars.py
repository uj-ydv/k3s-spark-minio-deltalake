from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
        .appName("Application-1") \
        .enableHiveSupport() \
        .getOrCreate()

# Get the list of jars as a Java Vector
jars_vector = spark.sparkContext._jsc.sc().listJars()
print("----------------------------------------------------------------------------------------------")
# Iterate through the Java Vector and print each jar on a new line
for i in range(jars_vector.size()):
    print(jars_vector.apply(i))
print("----------------------------------------------------------------------------------------------")
