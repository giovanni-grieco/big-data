python3 clean_dataset.py used_cars_data.csv
python3 drop_columns.py cleaned_used_cars_data.csv 0,1,2,3
python3 generate_portions.py pruned_cleaned_used_cars_data.csv 1,5,20