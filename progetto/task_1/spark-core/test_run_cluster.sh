HDFS_NODE=$(hdfs getconf -namenodes | awk '{print $1}' | cut -d':' -f1)

spark-submit \
        --master yarn \
        --deploy-mode cluster \
        --driver-memory 4g \
        --executor-memory 4g \
        --executor-cores 4 \
        spark-job.py \
        -i hdfs://${HDFS_NODE}:8020/user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv \
        -o hdfs://${HDFS_NODE}:8020/user/$USER/output/task1_spark_test_result \
