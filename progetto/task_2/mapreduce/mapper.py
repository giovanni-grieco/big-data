#!/usr/bin/env python3
"""mapper.py"""
import sys

skip_header = True

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
        print(f"{city}\t{year}\t{price}\t{daysonmarket}\t{description}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}\n")
        sys.stderr.write(f"Error: {e}\n")