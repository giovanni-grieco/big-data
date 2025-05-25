spark-submit \
    --master local[8] \
    spark-job.py \
    -i hdfs://localhost:9000/user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv \
    -o hdfs://localhost:9000/user/$USER/output/spark_cleaned_pruned_used_cars_data_1percent.csv \