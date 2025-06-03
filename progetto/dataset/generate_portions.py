import os
import sys
from tqdm import tqdm

def main():
    # Read the input file name from command line arguments
    input_file = sys.argv[1]
    portions = sys.argv[2].split(",")
    portions = [float(p) for p in portions]

    # Get file size for progress tracking
    file_size = os.path.getsize(input_file)
    
    # First pass: count total lines with progress bar
    total_lines = 0
    with tqdm(total=file_size, unit='B', unit_scale=True, 
             desc=f"Counting lines in {input_file}") as progress_bar:
        with open(input_file, 'r') as f:
            bytes_read = 0
            while line := f.readline():
                # Count the number of lines in the file
                total_lines += 1
                bytes_read += len(line)
                progress_bar.update(len(line))
    
    print(f"Total lines in the file: {total_lines}")
    
    # Create output file names
    input_file_names = [f"{input_file.split('.')[0]}_{int(p)}percent.csv" for p in portions]
    
    # Process each portion
    for portion, output_file_name in zip(portions, input_file_names):
        # Calculate the number of lines for the portion
        portion_lines = int(total_lines * (portion / 100))
        print(f"Creating {portion}% portion ({portion_lines} lines)")
        
        # Create the output file name with full path
        output_file_path = os.path.join(os.path.dirname(input_file), output_file_name)
        
        # Write the portion to the new file with progress bar
        with tqdm(total=portion_lines, unit='lines', 
                 desc=f"Generating {portion}% portion") as portion_progress:
            with open(output_file_path, 'w') as f_out:
                with open(input_file, 'r') as f_in:
                    i = 0
                    while i < portion_lines and (line := f_in.readline()):
                        f_out.write(line)
                        i += 1
                        portion_progress.update(1)
                        
            print(f"{portion}% portion written to {output_file_name}")

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 3:
        print("Usage: python generate_portions.py <input_file> <percentage_portion1,percentage_portion2,...>")
        sys.exit(1)
    
    # Call the main function
    main()