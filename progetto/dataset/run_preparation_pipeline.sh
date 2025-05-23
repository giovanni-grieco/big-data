#python3 clean_dataset.py used_cars_data.csv
#python3 drop_columns.py cleaned_used_cars_data.csv 8,10,12,14,28,42,45,48,65
#python3 generate_portions.py pruned_cleaned_used_cars_data.csv 1,5,20


python3 drop_columns.py used_cars_data.csv 7,10,12,14,27,42,45,48,65
python3 clean_dataset.py pruned_used_cars_data.csv false
python3 generate_portions.py cleaned_pruned_used_cars_data.csv 1,5,20