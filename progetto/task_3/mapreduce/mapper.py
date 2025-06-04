#!/usr/bin/env python3
"""mapper.py"""
import sys

skip_header = True

def generate_random_key_as_uuid():
    """Generate a random key for the mapper output."""
    import uuid
    return str(uuid.uuid4())
    

for line in sys.stdin:
    # Remove leading and trailing whitespace
    if skip_header:
        skip_header = False
        continue
    
    try:
        line = line.strip()
        cols = line.split(",") 
        model_name = cols[6]
        horsepower = cols[4]
        engine_displacement = cols[3]
        price = cols[7]
        
        # Emit the key-value pair
        print(f"{0}\t{model_name}\t{horsepower}\t{engine_displacement}\t{price}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}\n")
        sys.stderr.write(f"Error: {e}\n")