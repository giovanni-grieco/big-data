import time
import subprocess
import datetime
import os
import argparse

files = [
    "cleaned_pruned_used_cars_data_1percent",
    "cleaned_pruned_used_cars_data_5percent",
    "cleaned_pruned_used_cars_data_20percent",
    "cleaned_pruned_used_cars_data"
]

result_file_suffix="task2_sparkcore_result"

def generate_command(file, execution_mode):
    """Generate spark-submit command for the given file based on execution mode."""
    if execution_mode == "local":
        command = f"""
            spark-submit \
            --master local[*] \
            spark-job.py \
            -i hdfs://localhost:9000/user/$USER/input/{file}.csv \
            -o hdfs://localhost:9000/user/$USER/output/{file}_{result_file_suffix}
        """
    else:  # cluster mode for AWS EMR
        command = f"""
            HDFS_NODE=$(hdfs getconf -namenodes | awk '{"{print $1}"}' | cut -d':' -f1)
            spark-submit \
            --master yarn \
            --deploy-mode cluster \
            --driver-memory 4g \
            --executor-memory 4g \
            --executor-cores 4 \
            spark-job.py \
            -i hdfs://${"{HDFS_NODE}"}:8020/user/$USER/input/{file}.csv \
            -o hdfs://${"{HDFS_NODE}"}:8020/user/$USER/output/{file}_{result_file_suffix}
        """
    return command

def run_and_time(command, file_name, execution_mode):
    """Executes the command and measures execution time."""
    print(f"\n{'=' * 50}")
    print(f"Starting Spark experiment with file {file_name} in {execution_mode} mode")
    print(f"Start date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Command: {command}")
    print(f"{'=' * 50}\n")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Create names for log files and results
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    stdout_log = f"logs/{file_name}_{timestamp}_stdout.log"
    stderr_log = f"logs/{file_name}_{timestamp}_stderr.log"
    result_file = f"results/{file_name}_{timestamp}_{result_file_suffix}.txt"
    
    # Delete previous output if exists
    if execution_mode == "local":
        hdfs_path = f"hdfs://localhost:9000/user/$USER/output/{file_name}_{result_file_suffix}"
    else:
        # For cluster mode, use the HDFS namenode to construct the path
        hdfs_path = f"$(hdfs getconf -namenodes | awk '{{print $1}}' | cut -d':' -f1):8020/user/$USER/output/{file_name}_{result_file_suffix}"
    
    subprocess.run(f"hdfs dfs -rm -r -f /user/$USER/output/{file_name}_{result_file_suffix}", shell=True)
    
    # Measure execution time
    start_time = time.time()
    
    # Execute command and wait for completion
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Save output to log files
    with open(stdout_log, "wb") as f:
        f.write(process.stdout)
    
    with open(stderr_log, "wb") as f:
        f.write(process.stderr)
    
    # Check if command executed successfully
    if process.returncode == 0:
        status = "SUCCESS"
        
        # Save results from HDFS - adjust path based on mode
        print("Retrieving results from HDFS...")
        hdfs_cat_command = f"hdfs dfs -cat /user/$USER/output/{file_name}_{result_file_suffix}/part-*"
        
        hdfs_cat = subprocess.run(
            hdfs_cat_command,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if hdfs_cat.returncode == 0:
            with open(result_file, "wb") as f:
                f.write(hdfs_cat.stdout)
            print(f"Spark results saved to: {result_file}")
        else:
            print(f"Warning: Unable to retrieve results from HDFS")
            print(f"HDFS cat error: {hdfs_cat.stderr.decode()}")
            result_file = "N/A"
    else:
        status = "FAILED"
        print(f"Error: check log at {stderr_log}")
        print(f"Error message: {process.stderr.decode()}")
        result_file = "N/A"
    
    print(f"\n{'=' * 50}")
    print(f"Experiment with file {file_name} completed with status: {status}")
    print(f"Execution time: {execution_time:.2f} seconds ({datetime.timedelta(seconds=int(execution_time))})")
    print(f"End date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output saved to: {stdout_log}")
    print(f"Errors saved to: {stderr_log}")
    print(f"{'=' * 50}\n")
    
    return {
        "file_name": file_name,
        "status": status,
        "execution_time": execution_time,
        "start_time": start_time,
        "end_time": end_time,
        "stdout_log": stdout_log,
        "stderr_log": stderr_log,
        "result_file": result_file
    }

def main():
    # Setup command line argument parsing
    parser = argparse.ArgumentParser(description='Run Spark experiments on different dataset sizes')
    
    # Add mutually exclusive group for local/remote mode (one must be specified)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-l', '--local', action='store_true', help='Run in local mode')
    mode_group.add_argument('-c', '--remote', action='store_true', help='Run in cluster mode on AWS EMR')
    
    # Output file option
    parser.add_argument('-o', '--output', default='spark_results.csv',
                      help='Output CSV file to store results (default: spark_results.csv)')
    
    # File selection options
    parser.add_argument('-f', '--files', nargs='+', choices=files,
                      help='Specific file(s) to process (default: all files)')
    
    args = parser.parse_args()
    
    # Set execution mode based on arguments
    execution_mode = "local" if args.local else "remote"
    output_file = args.output
    
    # Use specified files or all files
    files_to_process = args.files if args.files else files
    
    print(f"Running in {execution_mode.upper()} mode")
    print(f"Processing files: {', '.join(files_to_process)}")
    print(f"Results will be saved to {output_file}")
    
    results = []
    overall_start = time.time()
    
    for file in files_to_process:
        command = generate_command(file, execution_mode)
        result = run_and_time(command, file, execution_mode)
        results.append(result)
    
    overall_end = time.time()
    overall_time = overall_end - overall_start
    
    # Print summary results
    print("\n\n" + "="*50)
    print("OVERALL RESULTS")
    print("="*50)
    print(f"{'Dataset':<35} {'Status':<10} {'Time (s)':<15}")
    print("-"*65)
    
    for result in results:
        print(f"{result['file_name']:<35} {result['status']:<10} {result['execution_time']:.2f}")
    
    print("-"*65)
    print(f"Total execution time: {overall_time:.2f} seconds ({datetime.timedelta(seconds=int(overall_time))})")
    print("="*50)
    
    # Save results to the specified CSV file
    with open(output_file, "w") as f:
        f.write("dataset,status,execution_time_seconds,stdout_log,stderr_log,result_file\n")
        for result in results:
            f.write(f"{result['file_name']},{result['status']},{result['execution_time']:.2f},{result['stdout_log']},{result['stderr_log']},{result['result_file']}\n")
    
    print(f"\nResults saved to {output_file}")
    print(f"Detailed logs are available in the 'logs/' directory")
    print(f"Spark job results are available in the 'results/' directory")

if __name__ == "__main__":
    main()