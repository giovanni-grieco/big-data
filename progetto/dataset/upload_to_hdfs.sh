hdfs dfs -mkdir -p /user/$USER/input
hdfs dfs -mkdir -p /user/$USER/output

hdfs dfs -put cleaned_pruned_used_cars_data_1percent.csv /user/$USER/input
hdfs dfs -put cleaned_pruned_used_cars_data_5percent.csv /user/$USER/input
hdfs dfs -put cleaned_pruned_used_cars_data_20percent.csv /user/$USER/input
hdfs dfs -put cleaned_pruned_used_cars_data.csv /user/$USER/input