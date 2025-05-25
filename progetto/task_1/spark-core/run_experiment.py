import time
import subprocess
import datetime
import sys
import os

files = [
    "cleaned_pruned_used_cars_data_1percent",
    "cleaned_pruned_used_cars_data_5percent",
    "cleaned_pruned_used_cars_data_20percent",
    "cleaned_pruned_used_cars_data"
]

def generate_command(file):
    """Generate spark-submit command for the given file."""
    command = f"""
        spark-submit \
        --master local[8] \
        spark-job.py \
        -i hdfs://localhost:9000/user/$USER/input/{file}.csv \
        -o hdfs://localhost:9000/user/$USER/output/spark_{file}_result
    """
    return command

def run_and_time(command, file_name):
    """Executes the command and measures execution time."""
    print(f"\n{'=' * 50}")
    print(f"Starting Spark experiment with file {file_name}")
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
    result_file = f"results/{file_name}_{timestamp}_result.txt"
    
    # Delete previous output if exists
    subprocess.run(f"hdfs dfs -rm -r -f /user/$USER/output/spark_{file_name}_result", shell=True)
    
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
        
        # Save results from HDFS
        print("Retrieving results from HDFS...")
        hdfs_cat = subprocess.run(
            f"hdfs dfs -cat /user/$USER/output/spark_{file_name}_result/part-*",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if hdfs_cat.returncode == 0:
            with open(result_file, "wb") as f:
                f.write(hdfs_cat.stdout)
            print(f"Spark results saved to: {result_file}")
        else:
            print(f"Warning: Unable to retrieve results from HDFS")
            result_file = "N/A"
    else:
        status = "FAILED"
        print(f"Error: check log at {stderr_log}")
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
    # Determine output file name
    output_file = "spark_results.csv"  # Default
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        print("You can specify the output filename as an argument.")
        print(f"Example: python {sys.argv[0]} <output_filename>\n")
    
    results = []
    overall_start = time.time()
    
    print(f"Starting Spark experiments on datasets of different sizes (results will be saved to {output_file})")
    
    for file in files:
        command = generate_command(file)
        result = run_and_time(command, file)
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