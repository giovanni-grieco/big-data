import sys
import re
import os
from tqdm import tqdm

def clean_line(line):
    #Remove [!@@Additional Info@@!]
    line = re.sub(r'\[!@@Additional Info@@!\]', '', line)
    line = re.sub(r'"([^"]*)"', lambda m: '"' + re.sub(r'[^a-zA-Z0-9_.,-]', ' ', m.group(1)) + '"', line)
    line = re.sub(r'"([^"]*)"', lambda m: m.group(0).replace(',', ' '), line)
    # Remove quotes from the header
    line = line.replace('"', '')
    line = line.replace("  ", " ")  # Replace multiple spaces with a single space
    line = line.lower()  # Convert to lowercase
    return line

def main():
    input_file = sys.argv[1]
    keep_header = True
    # Check if the user provided a second argument for keep_header
    if len(sys.argv) > 2:
        if sys.argv[2].lower() == 'false':
            keep_header = False
        elif sys.argv[2].lower() != 'true':
            print("Invalid argument for keep_header. Use 'true' or 'false'.")
            sys.exit(1)
    
    # Get file size for progress tracking
    file_size = os.path.getsize(input_file)
    
    with open(input_file, 'r') as f_in:
        with open(f"cleaned_{input_file}", 'w') as f_out:
            # Create progress bar
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True,
                              desc=f"Cleaning {input_file}")
            
            # remove illegal characters inside quotes, and then remove quotes
            # from the first line (header)
            first_line = True
            for line in f_in:
                if first_line:
                    if keep_header:
                        cleaned_line = clean_line(line)
                        f_out.write(cleaned_line)
                    first_line = False
                    # Update progress for first line
                    progress_bar.update(len(line))
                    continue
                
                # Process regular lines
                cleaned_line = clean_line(line)
                f_out.write(cleaned_line)
                # Update progress
                progress_bar.update(len(line))
            
            progress_bar.close()
            print(f"Finished cleaning. Output saved to cleaned_{input_file}")

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) < 2:
        print("Usage: python clean_dataset.py <input_file> <keep_header:Boolean - default=true>")
        sys.exit(1)
    
    # Call the main function
    main()