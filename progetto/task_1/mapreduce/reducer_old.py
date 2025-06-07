#!/usr/bin/env python3
"""reducer.py"""
import sys

model_2_price_sum = {}
model_2_count = {}

model_2_max_price = {}
model_2_min_price = {}

model_2_manufacturer = {}

model_2_years_set = {}


for line in sys.stdin:
    line = line.strip()

    manufacturer, model, price, year = line.split("\t")

    try:
        price = float(price)
        year = int(year)
    except ValueError:
        continue
    
    if model not in model_2_manufacturer:
        model_2_manufacturer[model] = manufacturer

    if model in model_2_price_sum:
        model_2_price_sum[model] += price
    else:
        model_2_price_sum[model] = price

    if model in model_2_count:
        model_2_count[model] += 1
    else:
        model_2_count[model] = 1

    if model in model_2_max_price:
        if price > model_2_max_price[model]:
            model_2_max_price[model] = price
    else:
        model_2_max_price[model] = price

    if model in model_2_min_price:
        if price < model_2_min_price[model]:
            model_2_min_price[model] = price
    else:
        model_2_min_price[model] = price

    if model in model_2_years_set:
        model_2_years_set[model].add(year)
    else:
        model_2_years_set[model] = {year}
        

model_2_avg_price = {}

for model in model_2_price_sum:
    avg_price = model_2_price_sum[model] / model_2_count[model]
    model_2_avg_price[model] = avg_price

for model in model_2_price_sum.keys():
    manufacturer = model_2_manufacturer[model]
    avg_price = model_2_avg_price[model]
    min_price = model_2_min_price[model]
    max_price = model_2_max_price[model]
    count = model_2_count[model]
    years = model_2_years_set[model]
    print(f"{manufacturer}\t{model}\t{count}\t{min_price}\t{max_price}\t{avg_price}\t{years}")
    



    