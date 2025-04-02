hdfs dfs -mkdir -p /user/$USER/input
hdfs dfs -mkdir -p /user/$USER/output
hdfs dfs -put input.txt /user/$USER/input/
hdfs dfs -ls /user/$USER/input

# Run the Hadoop streaming job
hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
    -input /user/$USER/input/input.txt \
    -output /user/$USER/output/wordcount_output \
    -mapper mapper.py \
    -reducer reducer.py \
