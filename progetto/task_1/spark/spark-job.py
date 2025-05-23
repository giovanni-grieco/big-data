from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder \
        .appName("task 1") \
        .getOrCreate()
    
    # Read the input data from HDFS
    

if __name__ == "__main__":
    main()