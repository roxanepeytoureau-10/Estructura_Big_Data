from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("ReadCSVFromHDFS") \
        .getOrCreate()

    # Path to your file in HDFS
    hdfs_path = "hdfs:///data/Superstore.csv"

    # Read CSV
    df = spark.read.csv(hdfs_path, header=True, inferSchema=True)

    # Show data
    df.show(10, truncate=False)

    # Print schema
    df.printSchema()

    spark.stop()

if __name__ == "__main__":
    main()
