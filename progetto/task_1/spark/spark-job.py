from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql import DataFrame
import argparse

def main():
    parser = argparse.ArgumentParser(description="Spark job to process data")
    parser.add_argument("-i", help="Path to the input file")
    parser.add_argument("-o", help="Path to the output file")
    args = parser.parse_args()


    spark = SparkSession.builder \
        .appName("task 1") \
        .getOrCreate()
    input_file = args.i
    output_file = args.o

    dataset = spark.textFile(input_file, header=True, inferSchema=True)
    


    # Read the input data from HDFS

if __name__ == "__main__":
    main()