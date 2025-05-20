#!/usr/bin/env python3
"""mapper.py"""
import sys
# Read each line from standard input
for line in sys.stdin:
    # Remove leading and trailing whitespace
    try:
        line = line.strip()
        cols = line.split(",") 
        manufacturer = cols[42].strip().strip('\t')
        model = cols[45].strip().strip('\t')
        price = cols[48].strip().strip('\t')
        year = cols[65].strip().strip('\t')
        print(f"{manufacturer}\t{model}\t{price}\t{year}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}\n")
        sys.stderr.write(f"Error: {e}\n")