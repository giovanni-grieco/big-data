#!/usr/bin/env python3
"""mapper.py"""
import sys
# Read each line from standard input

skip_header = True

for line in sys.stdin:
    # Remove leading and trailing whitespace

    if skip_header:
        skip_header = False
        continue
    try:
        line = line.strip()
        cols = line.split(",") 
        manufacturer = cols[5].strip().strip('\t')
        model = cols[6].strip().strip('\t')
        price = cols[7].strip().strip('\t')
        year = cols[8].strip().strip('\t')
        print(f"{manufacturer}\t{model}\t{price}\t{year}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}\n")
        sys.stderr.write(f"Error: {e}\n")