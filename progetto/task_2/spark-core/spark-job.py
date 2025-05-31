from pyspark.sql import SparkSession
from pyspark import SparkContext
import argparse

manufacturer_col = 5
model_col = 6
price_col = 7
year_col = 8

def reducer(a, b):
    car_count_a, daysonmarket_a, description_word2count_a, counter_a = a
    car_count_b, daysonmarket_b, description_word2count_b, counter_b = b
    # Combine counts and days on market
    added_car_count = car_count_a + car_count_b
    added_daysonmarket = daysonmarket_a + daysonmarket_b
    counter = counter_a + counter_b
    # Combine word counts from descriptions
    combined_description_word2count = description_word2count_a.copy()
    for word, count in description_word2count_b.items():
        combined_description_word2count[word] = combined_description_word2count.get(word, 0) + count
    return (added_car_count, added_daysonmarket, combined_description_word2count, counter)


def format_output(reduced_data):
    (city, year, price_range_code), (car_count, daysonmarket, description_word2count, counter) = reduced_data
    # Calculate average days on market
    if counter > 0:
        avg_daysonmarket = daysonmarket / counter
    else:
        avg_daysonmarket = 0

    #Extract the most common top 3 words from the description
    top_words = sorted(description_word2count.items(), key=lambda x: x[1], reverse=True)[:3]
    top_words_str = ", ".join([f"{word}({count})" for word, count in top_words])
    # Format the output as a string
    output = f"{city}\t{year}\t{decode_price_range(price_range_code)}\t{car_count}\t{avg_daysonmarket:.2f}\t{top_words_str}"
    return output

def description_to_word2count(description: str):
    # Split the description into words and count them
    words = description.split(" ")
    word_count = {}
    for word in words:
        word = word.lower()  # Normalize to lowercase
        if len(word) > 2:  # Filter out very short words
            word_count[word] = word_count.get(word, 0) + 1
    return word_count

def encode_price_range(price):
    if price < 20000:
        return 0
    if price >= 20000 and price < 50000:
        return 1
    if price >= 50000:
        return 2
    return -1

def decode_price_range(code):
    if code == 0:
        return "low_price_range"
    if code == 1:
        return "middle_price_range"
    if code == 2:
        return "high_price_range"
    return "unknown_price_range"

def mapper(line):
    try:
        cols = line.split(",")
        if len(cols) <= max(manufacturer_col, model_col, price_col, year_col):
            return None
        city = cols[0].strip()
        year = cols[8].strip()
        price = float(cols[7].strip())
        daysonmarket = int(cols[1].strip())
        description = cols[2].strip()
        description_word2count = description_to_word2count(description)
        price_range_code = encode_price_range(price)
        return ((city, year, price_range_code), (1, daysonmarket, description_word2count , 1))
    except (ValueError, IndexError):
        # If any error occurs during parsing, return None
        return None

def main():
    parser = argparse.ArgumentParser(description="Spark job to process data")
    parser.add_argument("-i", help="Path to the input file")
    parser.add_argument("-o", help="Path to the output file")
    args = parser.parse_args()
    spark :SparkSession = SparkSession.builder.appName("task 1").getOrCreate()
    input_file = args.i
    output_file = args.o
    dataset = spark.sparkContext.textFile(input_file)
    dataset = dataset.map(mapper) \
                    .filter(lambda x: x is not None) \
                    .reduceByKey(reducer) \
                    .map(format_output) \
                    .saveAsTextFile(output_file)

if __name__ == "__main__":
    main()