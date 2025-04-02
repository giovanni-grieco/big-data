#!/usr/bin/env python3
"""reducer.py"""
import sys

word_2_sum = {}

for line in sys.stdin:

    line = line.strip()

    word, count = line.split("\t")

    try:
        count = int(count)
    except ValueError:
        # If the count is not a number, skip this line
        continue
    # Check if the word is already in the dictionary
    # If it is, add the count to the existing count
    # If not, initialize it with the count

    # Sum the counts for each word
    if word in word_2_sum:
        word_2_sum[word] += count
    else:
        word_2_sum[word] = count

for word, count in word_2_sum.items():
    # Output the word and its total count
    print(f"{word}\t{count}")