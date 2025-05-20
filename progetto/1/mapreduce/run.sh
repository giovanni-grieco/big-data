hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_used_cars_data_1.csv\
    -output /user/$USER/output/cleaned_used_cars_data_1_result \
    -mapper mapper.py \
    -reducer reducer.py \