#!/usr/bin/env python3
"""mapper.py"""
import sys


city_year2_low_price_range_count = {}
city_year2_high_price_range_count = {}
city_year2_middle_price_range_count = {}

city_year2_low_price_range_sum_daysonmarket = {}
city_year2_middle_price_range_sum_daysonmarket = {}
city_year2_high_price_range_sum_daysonmarket = {}


def city_year2value_adder(key, daysonmakrket_price_range_dict, daysonmarket):
    if key not in daysonmakrket_price_range_dict:
        daysonmakrket_price_range_dict[key] = 0
    daysonmakrket_price_range_dict[key] = daysonmakrket_price_range_dict[key] + daysonmarket

def reduce_by_key(key, price, daysonmarket, description):
    if price < float(20000):
        city_year2value_adder(key, city_year2_low_price_range_count, 1)
        city_year2value_adder(key, city_year2_low_price_range_sum_daysonmarket, daysonmarket)
    
    elif price >= float(20000) and price < float(50000):
        city_year2value_adder(key, city_year2_middle_price_range_count, 1)
        city_year2value_adder(key, city_year2_middle_price_range_sum_daysonmarket, daysonmarket)
    
    elif price >= float(50000):
        city_year2value_adder(key, city_year2_high_price_range_count, 1)
        city_year2value_adder(key, city_year2_high_price_range_sum_daysonmarket, daysonmarket)

def collect_all_keys():
    keyset = set()
    keyset.update(city_year2_low_price_range_count.keys())
    keyset.update(city_year2_middle_price_range_count.keys())
    keyset.update(city_year2_high_price_range_count.keys())
    keyset.update(city_year2_low_price_range_sum_daysonmarket.keys())
    keyset.update(city_year2_middle_price_range_sum_daysonmarket.keys())
    keyset.update(city_year2_high_price_range_sum_daysonmarket.keys())
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

        print(f"{city}\t{year}\tlow_price_range\t{low_count}\t{avg_low_daysonmarket:.2f}")
        print(f"{city}\t{year}\tmiddle_price_range\t{middle_count}\t{avg_middle_daysonmarket:.2f}")
        print(f"{city}\t{year}\thigh_price_range\t{high_count}\t{avg_high_daysonmarket:.2f}")


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
        # Remove the debug print that might be cluttering output
        # print(f"{city}")
        reduce_by_key(key, price, daysonmarket, description)
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}, Error: {e}\n")

print_output()
