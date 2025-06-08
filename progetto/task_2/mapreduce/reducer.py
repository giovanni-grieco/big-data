#!/usr/bin/env python3
"""mapper.py"""
import sys
from collections import Counter
import re

city_year2_low_price_range_count = {}
city_year2_high_price_range_count = {}
city_year2_middle_price_range_count = {}

city_year2_low_price_range_sum_daysonmarket = {}
city_year2_middle_price_range_sum_daysonmarket = {}
city_year2_high_price_range_sum_daysonmarket = {}

# Add dictionaries to store word counts for each price range
city_year2_low_price_range_word_counts = {}
city_year2_middle_price_range_word_counts = {}
city_year2_high_price_range_word_counts = {}

def city_year2value_adder(key, daysonmakrket_price_range_dict, daysonmarket):
    if key not in daysonmakrket_price_range_dict:
        daysonmakrket_price_range_dict[key] = 0
    daysonmakrket_price_range_dict[key] = daysonmakrket_price_range_dict[key] + daysonmarket

def process_description(key, word_counts_dict, description):
    # Initialize Counter if key doesn't exist
    if key not in word_counts_dict:
        word_counts_dict[key] = Counter()
    
    # Extract words (without restricting to 3 characters)
    words = re.findall(r'\b[a-zA-Z0-9]+\b', description.lower())
    # Update word counts
    word_counts_dict[key].update(words)

def reduce_by_key(key, price, daysonmarket, description):
    if price < float(20000):
        city_year2value_adder(key, city_year2_low_price_range_count, 1)
        city_year2value_adder(key, city_year2_low_price_range_sum_daysonmarket, daysonmarket)
        process_description(key, city_year2_low_price_range_word_counts, description)
    
    elif price >= float(20000) and price < float(50000):
        city_year2value_adder(key, city_year2_middle_price_range_count, 1)
        city_year2value_adder(key, city_year2_middle_price_range_sum_daysonmarket, daysonmarket)
        process_description(key, city_year2_middle_price_range_word_counts, description)
    
    elif price >= float(50000):
        city_year2value_adder(key, city_year2_high_price_range_count, 1)
        city_year2value_adder(key, city_year2_high_price_range_sum_daysonmarket, daysonmarket)
        process_description(key, city_year2_high_price_range_word_counts, description)

def get_top_words(counter, top_n=3):
    # Get top N words
    top_words = [word for word, _ in counter.most_common(top_n)]
    return ", ".join(top_words) if top_words else "N/A"

def collect_all_keys():
    keyset = set()
    keyset.update(city_year2_low_price_range_count.keys())
    keyset.update(city_year2_middle_price_range_count.keys())
    keyset.update(city_year2_high_price_range_count.keys())
    return keyset

def print_output():
    keyset = collect_all_keys()
    for key in keyset:
        city, year = key
        # Use get() with default value to avoid KeyError
        low_count = city_year2_low_price_range_count.get(key, 0)
        middle_count = city_year2_middle_price_range_count.get(key, 0)
        high_count = city_year2_high_price_range_count.get(key, 0)
        low_sum_daysonmarket = city_year2_low_price_range_sum_daysonmarket.get(key, 0)
        middle_sum_daysonmarket = city_year2_middle_price_range_sum_daysonmarket.get(key, 0)
        high_sum_daysonmarket = city_year2_high_price_range_sum_daysonmarket.get(key, 0)

        avg_low_daysonmarket = low_sum_daysonmarket / low_count if low_count > 0 else 0
        avg_middle_daysonmarket = middle_sum_daysonmarket / middle_count if middle_count > 0 else 0
        avg_high_daysonmarket = high_sum_daysonmarket / high_count if high_count > 0 else 0

        # Get top words for each price range
        low_top_words = get_top_words(city_year2_low_price_range_word_counts.get(key, Counter()))
        middle_top_words = get_top_words(city_year2_middle_price_range_word_counts.get(key, Counter()))
        high_top_words = get_top_words(city_year2_high_price_range_word_counts.get(key, Counter()))

        print(f"{city}\t{year}\tlow_price_range\t{low_count}\t{avg_low_daysonmarket:.2f}\t{low_top_words}")
        print(f"{city}\t{year}\tmiddle_price_range\t{middle_count}\t{avg_middle_daysonmarket:.2f}\t{middle_top_words}")
        print(f"{city}\t{year}\thigh_price_range\t{high_count}\t{avg_high_daysonmarket:.2f}\t{high_top_words}")

errors = 0  # Initialize error counter
for line in sys.stdin:
    try:
        line = line.strip()
        parts = line.split("\t")
        
        # Handle input with different number of fields
        if len(parts) < 5:
            errors += 1
            continue
            
        city, year, price, daysonmarket, description = parts[0], parts[1], parts[2], parts[3], parts[4]
        try:
            price = float(price)
            daysonmarket = int(daysonmarket)
            year = int(year)  # Make sure year is consistently an integer
        except ValueError:
            errors += 1
            continue

        key = (city, year)  # Use consistent key format
        reduce_by_key(key, price, daysonmarket, description)
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}, Error: {e}\n")

print_output()