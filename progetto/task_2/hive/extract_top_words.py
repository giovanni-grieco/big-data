#!/usr/bin/env python3
# filepath: /home/giovanni/Projects/big-data/progetto/task_2/hive/extract_top_words.py

import sys
import re
from collections import Counter

# Process each line from stdin
for line in sys.stdin:
    try:
        # Split concatenated descriptions (they were joined with '|||')
        descriptions = line.strip().split('|||')
        
        # Tokenize words from all descriptions
        all_words = []
        for desc in descriptions:
            # Clean the text (remove special chars and convert to lowercase)
            clean_text = re.sub(r'[^\w\s]', ' ', desc.lower())
            words = [word for word in clean_text.split() if len(word) > 2]  # Filter out very short words
            all_words.extend(words)
        
        # Count word frequencies and get top 3
        word_counts = Counter(all_words)
        top_3_words = [word for word, _ in word_counts.most_common(3)]
        
        # Output the top 3 words as a comma-separated string
        print(','.join(top_3_words) if top_3_words else 'No words found')
        
    except Exception as e:
        # Output error for debugging
        print(f"Error: {str(e)}", file=sys.stderr)
        print("No words found")  # Fallback output