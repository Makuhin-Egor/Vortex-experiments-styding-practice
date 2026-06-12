import os
import re
import csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

LOG_DIR = os.path.join(BASE_DIR, "results", "raw_logs")
CSV_DIR = os.path.join(BASE_DIR, "results", "csv")
CSV_FILE = os.path.join(CSV_DIR, "experiment_data.csv")

def parse_logs():
    os.makedirs(CSV_DIR, exist_ok=True)
    
    results = []
    perf_regex = r"PERF: instrs=(\d+), cycles=(\d+), IPC=([\d\.]+)"
    
    if not os.path.exists(LOG_DIR):
        print(f"Error: Log directory not found at {LOG_DIR}")
        return

    for filename in sorted(os.listdir(LOG_DIR)):
        if filename.endswith(".log"):
            filepath = os.path.join(LOG_DIR, filename)
            with open(filepath, 'r') as f:
                content = f.read()
                matches = re.findall(perf_regex, content)
                if matches:
                    instrs, cycles, ipc = matches[-1]
                    
                    parts = filename.replace('.log', '').split('_')
                    app = parts[0]
                    scaling = parts[1]
                    cores = parts[2].replace('c', '')
                    cache = "No L2"
                    if "L2L3" in parts: 
                        cache = "L2+L3"
                    elif "L2" in parts: 
                        cache = "L2"
                    
                    l1_size = "16K"

                    results.append({
                        "Test Name": filename.replace('.log', ''),
                        "App": app,
                        "Scaling": scaling,
                        "Cores": int(cores),
                        "Cache": cache,
                        "L1 Size": l1_size,
                        "Cycles": int(cycles),
                        "IPC": float(ipc)
                    })

    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Test Name", "App", "Scaling", "Cores", "Cache", "L1 Size", "Cycles", "IPC"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Данные собраны и сохранены в {CSV_FILE}")

if __name__ == "__main__":
    parse_logs()