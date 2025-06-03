import kagglehub

# Download latest version
path = kagglehub.dataset_download("ananaymital/us-used-cars-dataset")

print("Path to dataset files:", path)