from pyspark.sql import SparkSession
from pyspark import SparkContext
import argparse

manufacturer_col = 5
model_col = 6
price_col = 7
year_col = 8

def reducer(a, b):
    manufacturer_a, price_a, year_set_a = a
    manufacturer_b, price_b, year_set_b = b
    
    manufacturer = manufacturer_a if manufacturer_a else manufacturer_b
    avg_price = (float(price_a) + float(price_b)) / 2
    years_set = year_set_a.union(year_set_b)

    return (manufacturer, avg_price, years_set)

def format_output(reduced_data):
    model, (manufacturer, avg_price, years_set) = reduced_data
    return f"{manufacturer}\t{model}\t{avg_price:.2f}\t{years_set}"

def parse_line(line):
    try:
        cols = line.split(",")
        if len(cols) <= max(manufacturer_col, model_col, price_col, year_col):
            return None
        model = cols[model_col]
        manufacturer = cols[manufacturer_col]
        price = float(cols[price_col])
        year = int(cols[year_col])
        
        return (model, (manufacturer, price, {year}))
    except (ValueError, IndexError):
        # If any error occurs during parsing, return None
        return None

def main():
    parser = argparse.ArgumentParser(description="Spark job to process data")
    parser.add_argument("-i", help="Path to the input file")
    parser.add_argument("-o", help="Path to the output file")
    args = parser.parse_args()

    spark :SparkSession = SparkSession.builder \
        .appName("task 1") \
        .getOrCreate()
    input_file = args.i
    output_file = args.o

    dataset = spark.sparkContext.textFile(input_file)
    
    dataset = dataset.map(lambda line: parse_line(line)) \
                    .filter(lambda x: x is not None) \
                    .reduceByKey(reducer) \
                    .map(format_output) \
                    .saveAsTextFile(output_file)

if __name__ == "__main__":
    main()