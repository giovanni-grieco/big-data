import sys
import re

def clean_line(line):
    line = re.sub(r'"([^"]*)"', lambda m: '"' + re.sub(r'[^a-zA-Z0-9_.,-]', '', m.group(1)) + '"', line)
    line = re.sub(r'"([^"]*)"', lambda m: m.group(0).replace(',', ' '), line)
    # Remove quotes from the header
    line = line.replace('"', '')
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
    with open(input_file, 'r') as f_in:
        with open(f"cleaned_{input_file}", 'w') as f_out:
            # remove illegal characters inside quotes, and then remove quotes
            # from the first line (header)
            first_line = True
            for line in f_in:
                if first_line:
                    if keep_header:
                        line = clean_line(line)
                        f_out.write(line)
                    first_line = False
                    continue
                line = clean_line(line)
                f_out.write(line)



if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 3:
        print("Usage: python clean_dataset.py <input_file> <keep_header:Boolean - default=true>")
        sys.exit(1)
    
    # Call the main function
    main()