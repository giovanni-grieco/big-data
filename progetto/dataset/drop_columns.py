import sys
import csv

def main():
    input_file = sys.argv[1]
    columns_to_keep = sys.argv[2].split(",")
    # Convert the column indices to integers
    columns_to_keep = [int(i) for i in columns_to_keep]
    
    with open(input_file, 'r', newline='') as f_in:
        with open(f"pruned_{input_file}", 'w', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            
            # Process each row
            for row in reader:
                try:
                    # Keep only the specified columns
                    pruned_row = [row[i] for i in columns_to_keep]
                    # Write the pruned row
                    writer.writerow(pruned_row)
                except Exception as e:
                    print(f"Error processing row: {row}")
                    print(f"Exception: {e}")
                    continue

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 3:
        print("Usage: python drop_columns.py <input_file> <col_to_keep1,col_to_keep2,...>")
        print("Example: python drop_columns.py input.csv 0,1,2,3,4,5,6,7,8")
        sys.exit(1)
    
    # Call the main function
    main()