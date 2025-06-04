#!/usr/bin/env python3
"""mapper.py"""
import sys

skip_header = True

def encode_price_in_range(price):
    if price < float(20000):
        return 0
    elif price >= float(20000) and price < float(50000):
        return 1
    elif price >= float(50000):
        return 2

for line in sys.stdin:
    # Remove leading and trailing whitespace
    if skip_header:
        skip_header = False
        continue
    
    try:
        line = line.strip()
        cols = line.split(",") 
        city = cols[0]
        year = cols[8]
        price = cols[7]
        daysonmarket = cols[1]
        description = cols[2]
        
        # Emit the key-value pair
        print(f"{city}::{year}::{encode_price_in_range(price)}\t{daysonmarket}\t{description}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}\n")
        sys.stderr.write(f"Error: {e}\n")