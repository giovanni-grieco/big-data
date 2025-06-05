#!/bin/bash

# Check if cluster_id.txt exists
if [ ! -f "cluster_id.txt" ]; then
    echo "Error: cluster_id.txt not found. Please create a cluster first."
    exit 1
fi

# Get the most recent cluster ID (last line of the file)
CLUSTER_ID=$(tail -n 1 cluster_id.txt)

echo "Getting master node DNS for cluster ID: $CLUSTER_ID"

# Get the master node DNS
MASTER_DNS=$(aws emr describe-cluster \
    --cluster-id "$CLUSTER_ID" \
    --query 'Cluster.MasterPublicDnsName' \
    --output text)

# Check if the command was successful
if [ $? -ne 0 ] || [ -z "$MASTER_DNS" ]; then
    echo "Error: Failed to retrieve master node DNS."
    echo "Make sure the cluster is running and you have the correct AWS credentials configured."
    exit 1
fi

echo "Master node DNS: $MASTER_DNS"
echo ""
echo "To SSH into the master node, use:"
echo "ssh -i ~/.ssh/desktop-fedora.pem hadoop@$MASTER_DNS"
echo ""
echo "To copy files to the master node, use:"
echo "scp -i ~/.ssh/desktop-fedora.pem /path/to/local/file hadoop@$MASTER_DNS:/path/on/master"
echo ""
echo "Master DNS has been saved to master_dns.txt"

# Save the DNS to a file for later use
echo "$MASTER_DNS" > master_dns.txt

# For easy copying, also print just the DNS on a line by itself
echo ""
echo "DNS only (for easy copying):"
echo "$MASTER_DNS"