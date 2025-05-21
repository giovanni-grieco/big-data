import sys


# Remove columns, keep certain columns
def main():
    input_file = sys.argv[1]
    columns_to_keep = sys.argv[2].split(",")
    # Convert the column indices to integers
    columns_to_keep = [int(i) for i in columns_to_keep]
    with open(input_file, 'r') as f:
        with open(f"pruned_{input_file}", 'w') as pruned_file:
            # Get the indices of the columns to keep
            # Write the data lines to the output file
            for line in f:
                line = line.strip()
                # Split the line into columns
                columns = line.split(",")
                # Keep only the specified columns
                pruned_columns = [columns[i] for i in columns_to_keep]
                # Write the pruned line to the output file
                pruned_file.write(",".join(pruned_columns) + "\n")

if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 3:
        print("Usage: python drop_columns.py <input_file> <col_to_keep1,col_to_keep2,...>")
        print("Example: python drop_columns.py input.csv 0,1,2,3,4,5,6,7,8")
        sys.exit(1)
    
    # Call the main function
    main()
