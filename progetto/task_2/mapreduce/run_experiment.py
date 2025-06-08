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

result_suffix = "task2_mapreduce_result"

def generate_command(file, execution_mode):
    if execution_mode == "local":
        command = f"""
            hadoop jar $HADOOP_HOME/streaming/hadoop-streaming.jar \
            -input /user/$USER/input/{file}.csv\
            -output /user/$USER/output/{file}_{result_suffix} \
            -mapper mapper.py \
            -reducer reducer.py \
        """
    else:  # remote mode for AWS EMR
        command = f"""
            hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
            -input /user/$USER/input/{file}.csv \
            -output /user/$USER/output/{file}_{result_suffix} \
            -file ./mapper.py \
            -file ./reducer.py \
            -mapper mapper.py \
            -reducer reducer_new.py
        """
    return command

def run_and_time(command, file_name):
    """Esegue il comando e misura il tempo di esecuzione."""
    print(f"\n{'=' * 50}")
    print(f"Avvio esperimento con file {file_name}")
    print(f"Data e ora di inizio: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Comando: {command}")
    print(f"{'=' * 50}\n")
    
    # Crea directory logs se non esiste
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Crea directory results se non esiste
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Crea nomi per i file di log e risultati
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    stdout_log = f"logs/{file_name}_{timestamp}_stdout.log"
    stderr_log = f"logs/{file_name}_{timestamp}_stderr.log"
    result_file = f"results/{file_name}_{timestamp}_{result_suffix}.txt"
    
    # Cancella l'output precedente se esiste
    subprocess.run(f"hdfs dfs -rm -r -f /user/$USER/output/{file_name}_{result_suffix}", shell=True)
    
    # Misura il tempo di esecuzione
    start_time = time.time()
    
    # Esegue il comando in modo bloccante (attende il completamento)
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Salva l'output in file di log
    with open(stdout_log, "wb") as f:
        f.write(process.stdout)
    
    with open(stderr_log, "wb") as f:
        f.write(process.stderr)
    
    # Verifica se il comando è stato eseguito con successo
    if process.returncode == 0:
        status = "SUCCESSO"
        
        # Salva i risultati dal HDFS
        print("Recupero risultati da HDFS...")
        hdfs_cat = subprocess.run(
            f"hdfs dfs -cat /user/$USER/output/{file_name}_{result_suffix}/part-*",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if hdfs_cat.returncode == 0:
            with open(result_file, "wb") as f:
                f.write(hdfs_cat.stdout)
            print(f"Risultati MapReduce salvati in: {result_file}")
        else:
            print(f"Attenzione: Impossibile recuperare i risultati da HDFS")
            result_file = "N/A"
    else:
        status = "FALLITO"
        print(f"Errore: controlla il log in {stderr_log}")
        result_file = "N/A"
    
    print(f"\n{'=' * 50}")
    print(f"Esperimento con file {file_name} completato con {status}")
    print(f"Tempo di esecuzione: {execution_time:.2f} secondi ({datetime.timedelta(seconds=int(execution_time))})")
    print(f"Data e ora di fine: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output salvato in: {stdout_log}")
    print(f"Errori salvati in: {stderr_log}")
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
    parser = argparse.ArgumentParser(description='Run MapReduce experiments on different dataset sizes')
    
    # Add mutually exclusive group for local/remote mode (one must be specified)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-l', '--local', action='store_true', help='Run in local mode')
    mode_group.add_argument('-r', '--remote', action='store_true', help='Run in remote mode on AWS EMR')
    
    # Output file option
    parser.add_argument('-o', '--output', default='mapreduce_results.csv',
                      help='Output CSV file to store results (default: mapreduce_results.csv)')
    
    args = parser.parse_args()
    
    # Set execution mode based on arguments
    execution_mode = "local" if args.local else "remote"
    output_file = args.output
    
    print(f"Running in {execution_mode.upper()} mode")
    print(f"Results will be saved to {output_file}")
    
    results = []
    overall_start = time.time()
    
    for file in files:
        command = generate_command(file, execution_mode)
        result = run_and_time(command, file)
        results.append(result)
    
    overall_end = time.time()
    overall_time = overall_end - overall_start
    
    # Stampa risultati riassuntivi
    print("\n\n" + "="*50)
    print("RISULTATI COMPLESSIVI")
    print("="*50)
    print(f"{'Dataset':<35} {'Stato':<10} {'Tempo (s)':<15}")
    print("-"*65)
    
    for result in results:
        print(f"{result['file_name']:<35} {result['status']:<10} {result['execution_time']:.2f}")
    
    print("-"*65)
    print(f"Tempo totale di esecuzione: {overall_time:.2f} secondi ({datetime.timedelta(seconds=int(overall_time))})")
    print("="*50)
    
    # Salva i risultati nel file CSV specificato
    with open(output_file, "w") as f:
        f.write("dataset,status,execution_time_seconds,stdout_log,stderr_log,result_file\n")
        for result in results:
            f.write(f"{result['file_name']},{result['status']},{result['execution_time']:.2f},{result['stdout_log']},{result['stderr_log']},{result['result_file']}\n")
    
    print(f"\nRisultati salvati in {output_file}")
    print(f"I log dettagliati sono disponibili nella directory 'logs/'")
    print(f"I risultati dei job MapReduce sono disponibili nella directory 'results/'")

if __name__ == "__main__":
    main()