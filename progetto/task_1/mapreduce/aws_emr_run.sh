#!/bin/bash

aws s3 cp ./mapper.py ${BUCKET_S3}/task_1/mapper.py
aws s3 cp ./reducer.py ${BUCKET_S3}/task_1/reducer.py

MAPPER="${BUCKET_S3}/task_1/mapper.py"
REDUCER="${BUCKET_S3}/task_1/reducer.py"
INPUT="${BUCKET_S3}/cleaned_pruned_used_cars_data_1percent.csv"
OUTPUT="${BUCKET_S3}/user/$USER/output/task1_mapreduce_result"

# Run the MapReduce job on the EMR cluster
aws emr add-steps \
    --cluster-id $(cat ../../aws-emr/cluster_id.txt) \
    --steps '[{
        "Type": "STREAMING",
        "Name": "Task 1 MapReduce",
        "ActionOnFailure": "CONTINUE",
        "Args": [
            "-files", "'${MAPPER},${REDUCER}'",
            "-mapper", "mapper.py",
            "-reducer", "reducer.py",
            "-input", "'${INPUT}'",
            "-output", "'${OUTPUT}'"
        ]
    }]'