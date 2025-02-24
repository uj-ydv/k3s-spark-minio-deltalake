from pyspark.sql import SparkSession

def main():
    # Initialize Spark Session connecting to Kyuubi
    spark = SparkSession.builder \
        .appName("Read Delta Table from Kyuubi") \
        .config("spark.kyuubi.session.connection.url", "kyuubi:10009") \
        .getOrCreate()

    # Define the Delta table name
    delta_table_name = "wba.health_table"

    # Read the Delta table into a DataFrame via Kyuubi
    health_df = spark.table(delta_table_name)

    # Filter records where Obesity > 30
    high_obesity_df = health_df.filter("Obesity > 30")

    # Show the first 5 rows of the filtered DataFrame
    print("High obesity records:")
    high_obesity_df.show(5)

if __name__ == "__main__":
    main()
