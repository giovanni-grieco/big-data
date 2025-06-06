hdfs dfs -mkdir -p /task_2/hive/
hdfs dfs -put extract_top_words.py /task_2/hive/

hive -hivevar input_path=/user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv -f ./task.hql