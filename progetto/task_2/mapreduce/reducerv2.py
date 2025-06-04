#!/usr/bin/env python3
"""mapper.py"""
import sys


for line in sys.stdin:
    line = line.strip()
    header, daysonmarket, description = line.split("\t")
    city, year, price_range = header.split("::")