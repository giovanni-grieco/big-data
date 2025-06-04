#!/usr/bin/env python3
"""mapper.py"""
import sys



for line in sys.stdin:
    line = line.strip()
    id, model_name, horsepower, engine_displacement, price = line.split("\t")
    