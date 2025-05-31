hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
        -input /user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv \
        -output /user/$USER/output/task1_mapreduce_test_result \
        -mapper mapper.py \
        -reducer reducer.py \