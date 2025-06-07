#!/usr/bin/env python3
"""reducer.py"""
import sys

class Stats:
    def __init__(self):
        self.price_sum = 0
        self.price_min = float('inf')
        self.price_max = float('-inf')
        self.years = set()
        self.count = 0

manufacturer_model2stats={}

def update_stats(manufacturer_model, price, year):
    if manufacturer_model not in manufacturer_model2stats:
        manufacturer_model2stats[manufacturer_model] = Stats()
    
    stats = manufacturer_model2stats[manufacturer_model]
    stats.price_sum += price
    stats.count += 1
    stats.years.add(year)
    
    if price < stats.price_min:
        stats.price_min = price
    if price > stats.price_max:
        stats.price_max = price

for line in sys.stdin:
    line = line.strip()
    
    try:
        manufacturer_model, price, year = line.split("\t")
        price = float(price)
        year = int(year)
        if price < 0:
            sys.stderr.write(f"Negative price encountered: {price} for {manufacturer_model}\n")
            continue
        update_stats(manufacturer_model, price, year)
        
    except ValueError:
        sys.stderr.write(f"{ValueError}\n")
        continue


for manufacturer_model, stats in manufacturer_model2stats.items():
    avg_price = stats.price_sum / stats.count if stats.count > 0 else 0
    manufacturer, model = manufacturer_model.split("::")
    print(f"{manufacturer}\t{model}\t{stats.count}\t{avg_price:.2f}\t{stats.price_min:.2f}\t{stats.price_max:.2f}\t{stats.years}")



    