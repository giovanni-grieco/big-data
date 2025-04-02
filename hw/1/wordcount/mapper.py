#!/usr/bin/env python3
"""mapper.py"""
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()

    for word in words:
        # Output each word with a count of 1
        print(f"{word}\t1")