import sys
import re

def main():
    input_file = sys.argv[1]
    with open(input_file, 'r', newline='') as f_in:
        with open(f"cleaned_{input_file}", 'w', newline='') as f_out:
            # remove illegal characters inside quotes, and then remove quotes
            # from the first line (header)
            first_line = True
            for line in f_in:
                if first_line:
                    first_line = False
                    # Remove illegal characters inside quotes
                    line = re.sub(r'"([^"]*)"', lambda m: '"' + re.sub(r'[^a-zA-Z0-9_.,-]', '', m.group(1)) + '"', line)
                    # Remove quotes from the header
                    line = line.replace('"', '')
                else:
                    # Remove illegal characters inside quotes
                    line = re.sub(r'"([^"]*)"', lambda m: '"' + re.sub(r'[^a-zA-Z0-9_.,-]', '', m.group(1)) + '"', line)
                f_out.write(line)



if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 2:
        print("Usage: python clean_dataset.py <input_file>")
        sys.exit(1)
    
    # Call the main function
    main()