#!/bin/bash
aws s3 cp cleaned_pruned_used_cars_data_1percent.csv ${BUCKET_S3}/cleaned_pruned_used_cars_data_1percent.csv
aws s3 cp cleaned_pruned_used_cars_data_5percent.csv ${BUCKET_S3}/cleaned_pruned_used_cars_data_5percent.csv
aws s3 cp cleaned_pruned_used_cars_data_20percent.csv ${BUCKET_S3}/cleaned_pruned_used_cars_data_20percent.csv
aws s3 cp cleaned_pruned_used_cars_data.csv ${BUCKET_S3}/cleaned_pruned_used_cars_data.csv