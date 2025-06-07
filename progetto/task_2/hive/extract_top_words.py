#!/usr/bin/env python3

import sys
import re
from collections import Counter

# Process each line from stdin
for line in sys.stdin:
    try:
        # Parse the input (tab-delimited)
        fields = line.strip().split('\t')
        if len(fields) < 6:
            print("Invalid input format", file=sys.stderr)
            continue
            
        # Extract fields
        city = fields[0]
        year = fields[1]
        price_range = fields[2]
        num_cars = fields[3]
        avg_daysonmarket = fields[4]
        descriptions = fields[5].split('|||')
        
        # Process descriptions to find top words
        all_words = []
        for desc in descriptions:
            # Clean the text (remove special chars and convert to lowercase)
            if desc:
                clean_text = re.sub(r'[^\w\s]', ' ', desc.lower())
                words = [word for word in clean_text.split() if len(word) > 2]  # Filter out very short words
                all_words.extend(words)
        
        # Count word frequencies and get top 3
        word_counts = Counter(all_words)
        top_3_words = [word for word, _ in word_counts.most_common(3)]
        top_words_str = ','.join(top_3_words) if top_3_words else 'No words found'
        
        # Output all fields including the processed top words
        print(f"{city}\t{year}\t{price_range}\t{num_cars}\t{avg_daysonmarket}\t{top_words_str}")
        
    except Exception as e:
        # Output error for debugging
        pass