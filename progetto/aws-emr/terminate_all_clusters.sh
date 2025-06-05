#!/bin/bash
# Terminate all EMR clusters taking the IDs from cluster_id.txt
if [ ! -f cluster_id.txt ]; then
    echo "cluster_id.txt not found. Please create a cluster first."
    exit 1
fi
while IFS= read -r cluster_id; do
    echo "Terminating cluster with ID: $cluster_id"
    aws emr terminate-clusters --cluster-ids "$cluster_id"
done < cluster_id.txt

# Remove the cluster_id.txt file after termination
rm -f cluster_id.txt
echo "All clusters terminated and cluster_id.txt removed."