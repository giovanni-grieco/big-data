#!/usr/bin/env python3
"""mapper.py"""
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()

    for i in range(len(words)):
        # Check if the next word exists
        if i + 1 < len(words):
            # Output the bigram with a count of 1
            print(f"{words[i]} {words[i + 1]}\t1")