#!/bin/bash

# Clean up previous outputs
hdfs dfs -rm -r -f /task_2
hdfs dfs -mkdir -p /task_2/hive/
hdfs dfs -put extract_top_words.py /task_2/hive/

# Enable verbose logging and save output
hive -hivevar input_path=/user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv \
     -hiveconf hive.root.logger=INFO,console \
     -hiveconf mapreduce.job.queuename=default \
     -f ./task.hql 2>&1 | tee hive_run_$(date +%Y%m%d_%H%M%S).log