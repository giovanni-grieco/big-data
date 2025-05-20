hdfs dfs -mkdir -p /user/$USER/input
hdfs dfs -mkdir -p /user/$USER/output
hdfs dfs -put cleaned_used_cars_data.csv /user/$USER/input/
hdfs dfs -put cleaned_used_cars_data_1.csv /user/$USER/input/
hdfs dfs -put cleaned_used_cars_data_5.csv /user/$USER/input/
hdfs dfs -put cleaned_used_cars_data_20.csv /user/$USER/input/