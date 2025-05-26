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
        daysonmakrket_price_range_dict[key]=0
    daysonmakrket_price_range_dict[key]=daysonmakrket_price_range_dict[key]+daysonmarket

def reduce_by_key(key, price, daysonmarket, description):
    if price < float(20000):
        city_year2value_adder(key, city_year2_low_price_range_count, 1)
        city_year2value_adder(key, city_year2_low_price_range_sum_daysonmarket, daysonmarket)
    
    elif price >= float(20000) and price < float(50000):
        city_year2value_adder(key,city_year2_middle_price_range_count, 1)
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
    for (city, year) in keyset:
        low_count = city_year2_low_price_range_count[(city, year)]
        middle_count = city_year2_middle_price_range_count[(city, year)]
        high_count = city_year2_high_price_range_count[(city, year)]
        low_sum_daysonmarket = city_year2_low_price_range_sum_daysonmarket[(city, year)]
        middle_sum_daysonmarket = city_year2_middle_price_range_sum_daysonmarket[(city, year)]
        high_sum_daysonmarket = city_year2_high_price_range_sum_daysonmarket[(city, year)]

        avg_low_daysonmarket = low_sum_daysonmarket / low_count if low_count > 0 else 0
        avg_middle_daysonmarket = middle_sum_daysonmarket / middle_count if middle_count > 0 else 0
        avg_high_daysonmarket = high_sum_daysonmarket / high_count if high_count > 0 else 0

        print(f"{city}\t{year}\tlow_price_range\t{low_count}\t{avg_low_daysonmarket:.2f}")
        print(f"{city}\t{year}\tmiddle_price_range\t{middle_count}\t{avg_middle_daysonmarket:.2f}")
        print(f"{city}\t{year}\thigh_price_range\t{high_count}\t{avg_high_daysonmarket:.2f}")


for line in sys.stdin:
    line = line.strip()

    city, year, price, daysonmarket, description = line.split("\t")
    try:
        price = float(price)
        daysonmarket = int(daysonmarket)
    except ValueError:
        continue

    key = (city, year)
    reduce_by_key(key, price, daysonmarket, description)
    print_output()

    

    

