import sys
import csv
import os
from tqdm import tqdm

def main():
    input_file = sys.argv[1]
    columns_to_keep = sys.argv[2].split(",")
    # Convert the column indices to integers
    columns_to_keep = [int(i) for i in columns_to_keep]
    
    # Get file size for progress tracking
    file_size = os.path.getsize(input_file)
    
    with open(input_file, 'r', newline='') as f_in:
        with open(f"pruned_{input_file}", 'w', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            
            # Create progress bar
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, 
                               desc=f"Processing {input_file}")
            
            # Process each row
            processed_bytes = 0
            for row in reader:
                try:
                    # Keep only the specified columns
                    pruned_row = [row[i] for i in columns_to_keep]
                    # Write the pruned row
                    writer.writerow(pruned_row)
                    
                    # Update progress based on line length
                    line_size = sum(len(field) for field in row) + len(row)  # Include commas
                    processed_bytes += line_size
                    progress_bar.update(line_size)
                    
                except Exception as e:
                    print(f"Exception: {e}")
                    continue
            
            progress_bar.close()
            print(f"Finished processing. Output saved to pruned_{input_file}")

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 3:
        print("Usage: python drop_columns.py <input_file> <col_to_keep1,col_to_keep2,...>")
        print("Example: python drop_columns.py input.csv 0,1,2,3,4,5,6,7,8")
        sys.exit(1)
    
    # Call the main function
    main()