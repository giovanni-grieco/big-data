#!/bin/bash

# Create a temporary file to store the JSON output
tmp_output=$(mktemp)

# Run the EMR create-cluster command and save output to the temp file
aws emr create-cluster \
    --name "big-data-cluster" \
    --release-label emr-7.9.0 \
    --applications Name=Hadoop Name=Spark Name=Hive \
    --use-default-roles \
    --ec2-attributes KeyName=desktop-fedora \
    --instance-type m5.xlarge \
    --instance-count 3 \
    --log-uri ${BUCKET_S3}/logs/ \
    --auto-terminate > $tmp_output

# Extract the ClusterId from the JSON output
cluster_id=$(cat $tmp_output | jq -r '.ClusterId')

# Append only the cluster ID to the cluster_id.txt file
echo $cluster_id >> cluster_id.txt

# Print confirmation
echo "Cluster created with ID: $cluster_id"
echo "ID saved to cluster_id.txt"

# Clean up the temporary file
rm $tmp_output