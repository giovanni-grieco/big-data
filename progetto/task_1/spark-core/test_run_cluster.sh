spark-submit \
        --master yarn \
        --deploy-mode cluster \
        --driver-memory 4g \
        --executor-memory 4g \
        --executor-cores 4 \
        spark-job.py \
        -i hdfs://ec2-18-195-217-145.eu-central-1.compute.amazonaws.com:9000/user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv \
        -o hdfs://ec2-18-195-217-145.eu-central-1.compute.amazonaws.com:9000/user/$USER/output/task1_spark_test_result \
