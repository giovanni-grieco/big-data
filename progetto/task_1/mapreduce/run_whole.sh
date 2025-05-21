hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_pruned_used_cars_data_1percent.csv\
    -output /user/$USER/output/cleaned_pruned_used_cars_data_1percent_result \
    -mapper mapper.py \
    -reducer reducer.py \

hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_pruned_used_cars_data_5percent.csv\
    -output /user/$USER/output/cleaned_pruned_used_cars_data_5percent_result \
    -mapper mapper.py \
    -reducer reducer.py \

hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_pruned_used_cars_data_20percent.csv\
    -output /user/$USER/output/cleaned_pruned_used_cars_data_20percent_result \
    -mapper mapper.py \
    -reducer reducer.py \

hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_pruned_used_cars_data.csv\
    -output /user/$USER/output/cleaned_pruned_used_cars_data_result \
    -mapper mapper.py \
    -reducer reducer.py \
