# Create 1%, 5%, 20% versions of a csv dataset

import os
import sys

def main():
    # Read the input file name from command line arguments
    input_file = sys.argv[1]
    

    total_lines = 0
    # Read the input file
    with open(input_file, 'r') as f:
        while line := f.readline():
            # Count the number of lines in the file
            total_lines += 1
    print(f"Total lines in the file: {total_lines}")
    # Calculate the number of lines for each portion

    portion_1 = int(total_lines * 0.01)
    portion_5 = int(total_lines * 0.05)
    portion_20 = int(total_lines * 0.20)
    
    # Create output directories if they don't exist
    input_file_name1 = input_file.split(".")[0]+"_1.csv"
    input_file_name5 = input_file.split(".")[0]+"_5.csv"
    input_file_name20 = input_file.split(".")[0]+"_20.csv"
    
    # Write the 1% portion to a new file
    with open(input_file_name1, 'w') as f:
        with open(input_file, 'r') as original_file:
            i = 0
            while line := original_file.readline():
                if i < portion_1:
                    f.write(line)
                    i += 1
                else:
                    break
        print(f"1% portion written to {input_file_name1}")
    
    # Write the 5% portion to a new file
    with open(input_file_name5, 'w') as f:
        with open(input_file, 'r') as original_file:
            i = 0
            while line := original_file.readline():
                if i < portion_5:
                    f.write(line)
                    i += 1
                else:
                    break
        print(f"5% portion written to {input_file_name5}")
    
    # Write the 20% portion to a new file
    with open(input_file_name20, 'w') as f:
        with open(input_file, 'r') as original_file:
            i = 0
            while line := original_file.readline():
                if i < portion_20:
                    f.write(line)
                    i += 1
                else:
                    break
        print(f"20% portion written to {input_file_name20}")

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 2:
        print("Usage: python generate_portions.py <input_file>")
        sys.exit(1)
    
    # Call the main function
    main()