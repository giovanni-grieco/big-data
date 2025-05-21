import sys
import csv

def main():
    input_file = sys.argv[1]
    with open(input_file, 'r', newline='') as f_in:
        with open(f"cleaned_{input_file}", 'w', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            # Skip header
            next(reader, None)
            # Process and write each row
            for row in reader:
                writer.writerow(row)


if __name__ == "__main__":
    # Check if the script is being run directly
    if len(sys.argv) != 2:
        print("Usage: python clean_dataset.py <input_file>")
        sys.exit(1)
    
    # Call the main function
    main()