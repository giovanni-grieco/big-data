hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_used_cars_data_1.csv\
    -output /user/$USER/output/cleaned_used_cars_data_1_result \
    -mapper mapper.py \
    -reducer reducer.py \

hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_used_cars_data_5.csv\
    -output /user/$USER/output/cleaned_used_cars_data_5_result \
    -mapper mapper.py \
    -reducer reducer.py \

hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_used_cars_data_20.csv\
    -output /user/$USER/output/cleaned_used_cars_data_20_result \
    -mapper mapper.py \
    -reducer reducer.py \

hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/cleaned_used_cars_data.csv\
    -output /user/$USER/output/cleaned_used_cars_data_result \
    -mapper mapper.py \
    -reducer reducer.py \