hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/pruned_used_cars_data_1percent.csv\
    -output /user/$USER/output/pruned_used_cars_data_1percent_result \
    -mapper mapper.py \
    -reducer reducer.py \