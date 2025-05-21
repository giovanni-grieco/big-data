#!/usr/bin/env python3
"""mapper.py"""
import sys
import csv
# Read each line from standard input

first_line = True
for line in sys.stdin:
    # Skip the first line (header)
    if first_line:
        first_line = False
        continue
    try:
        line = line.strip()
        csv 
        

        print(f"{manufacturer}\t{model}\t{price}\t{year}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}\n")
        sys.stderr.write(f"Error: {e}\n")