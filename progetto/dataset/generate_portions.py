# Create 1%, 5%, 20% versions of a csv dataset

import os
import sys

def main():
    # Read the input file name from command line arguments
    input_file = sys.argv[1]
    
    portions = sys.argv[2].split(",")

    total_lines = 0
    # Read the input file
    with open(input_file, 'r') as f:
        while line := f.readline():
            # Count the number of lines in the file
            total_lines += 1
    print(f"Total lines in the file: {total_lines}")
    # Calculate the number of lines for each portion

    portions = [float(p) for p in portions]
    
    # Create output directories if they don't exist
    input_file_names = [f"{input_file.split('.')[0]}_{int(p)}percent.csv" for p in portions]
    
    # Write the 1% portion to a new file
    for portion, input_file_name in zip(portions, input_file_names):
        # Calculate the number of lines for the portion
        portion_lines = int(total_lines * (portion / 100))
        print(f"Portion: {portion}")
        
        # Create the output file name
        input_file_name = os.path.join(os.path.dirname(input_file), input_file_name)
        
        # Write the portion to the new file
        with open(input_file_name, 'w') as f:
            with open(input_file, 'r') as original_file:
                i = 0
                while line := original_file.readline():
                    if i < portion_lines:
                        f.write(line)
                        i += 1
                    else:
                        break
            print(f"{portion} portion written to {input_file_name}")
    

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 3:
        print("Usage: python generate_portions.py <input_file> <percentage_portion1,percentage_portion2,...>")
        sys.exit(1)
    
    # Call the main function
    main()