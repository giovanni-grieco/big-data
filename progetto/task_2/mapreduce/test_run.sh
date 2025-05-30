hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
        -input /user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv\
        -output /user/$USER/output/cleaned_pruned_used_cars_data_1percent_task2_mapreduce_results \
        -mapper mapper.py \
        -reducer reducer.py \