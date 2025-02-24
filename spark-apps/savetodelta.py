from delta.tables import DeltaTable
from pyspark.sql import SparkSession

def main():

    source_bucket = "wba"

    spark = SparkSession.builder \
        .appName("CSV File to Delta Lake Table") \
        .enableHiveSupport() \
        .getOrCreate()

    input_path = f"s3a://{source_bucket}/test-data/Air_Quality.csv"
    input1_path = f"s3a://{source_bucket}/test-data/people-100.csv"
    input2_path = f"s3a://{source_bucket}/test-data/Lottery_Powerball_Winning_Numbers__Beginning_2010.csv"
    input3_path = f"s3a://{source_bucket}/test-data/LakeCounty_Health_-6177935595181947989.csv"
    delta_path = f"s3a://{source_bucket}/delta/wba/tables/"

    # Drop the schema if it exists and create it again
    spark.sql("DROP SCHEMA IF EXISTS wba CASCADE")
    spark.sql("CREATE DATABASE IF NOT EXISTS wba")
    spark.sql("USE wba")

    # Read CSV files into DataFrames
    df_air_quality = spark.read.csv(input_path, header=True, inferSchema=True)
    df_people = spark.read.csv(input1_path, header=True, inferSchema=True)
    df_lottery = spark.read.csv(input2_path, header=True, inferSchema=True)
    df_health = spark.read.csv(input3_path, header=True, inferSchema=True)

    # Function to save DataFrame as Delta Table with existence check
    def save_as_delta_table(df, table_name, path):
        if DeltaTable.isDeltaTable(spark, path):
            print(f"Dropping existing Delta table: {table_name}")
            spark.sql(f"DROP TABLE IF EXISTS {table_name}")
        
        df.write.format("delta").mode("overwrite") \
            .option("delta.columnMapping.mode", "name") \
            .option("path", path) \
            .saveAsTable(table_name)

    # Write each DataFrame to a Delta table
    save_as_delta_table(df_air_quality, "wba.air_quality_table", f"{delta_path}/air_quality_table")
    save_as_delta_table(df_people, "wba.people_table", f"{delta_path}/people_table")
    save_as_delta_table(df_lottery, "wba.lottery_table", f"{delta_path}/lottery_table")
    save_as_delta_table(df_health, "wba.health_table", f"{delta_path}/health_table")

    # Optional: Show the contents of each Delta table
    DeltaTable.forName(spark, "wba.air_quality_table").toDF().show()
    DeltaTable.forName(spark, "wba.people_table").toDF().show()
    DeltaTable.forName(spark, "wba.lottery_table").toDF().show()
    DeltaTable.forName(spark, "wba.health_table").toDF().show()

if __name__ == "__main__":
    main()
