import sys
import re

def main():
    input_file = sys.argv[1]
    # Read the input file
    first_line = True
    with open(input_file, 'r') as f:
        with open(f"cleaned_{input_file}", 'w') as cleaned_file:
            while line := f.readline():
                if first_line:
                    # Skip the header line
                    first_line = False
                    continue
                #Some columns have text with quotation marks, and inside these text commas are not delimiters
                #So we will remove the commas inside the quotation marks and 
                # Remove leading and trailing whitespace
                line = line.strip()
                # Split the line using a regex that takes into account the quotation marks
                # find where a inside a pair of quotes there are commas, remove the comma(s)
                line = re.sub(r'"([^"]*)"', lambda m: m.group(0).replace(",", ""), line)
                # Remove the quotes in pair of quotes
                line = re.sub(r'"([^"]*)"', r'\1', line)
                cleaned_file.write(line+"\n")


if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 2:
        print("Usage: python clean_dataset.py <input_file>")
        sys.exit(1)
    
    # Call the main function
    main()