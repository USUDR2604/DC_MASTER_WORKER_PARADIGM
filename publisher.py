# publishing details 
import json
from xmlrpc.client import ServerProxy
import time
# Function to publish data records to workers
def publish_data_record():
    # Load data from JSON files
    with open("data-am.json", "r") as file1:
        data_1 = json.load(file1)
    with open("data-nz.json", "r") as file2:
        data_2 = json.load(file2)
    
    # Connect to each worker with its ports
    worker_1 = ServerProxy("http://localhost:23001/")
    worker_2 = ServerProxy("http://localhost:23002/")
    
    # Publishing data to worker 1 with delay
    for i in data_1.items():
        try:
            worker_1.PublishData(i)
            time.sleep(2)
        except Exception as e:
            print(f"Error publishing record {i} to worker 1:", e)

    # Publishing data to worker 2 with delay
    for i in data_2.items():
        try:
            worker_2.PublishData(data_2[i])
            time.sleep(2)
        except Exception as e:
            print(f"Error publishing record {i} to worker 2:", e)

publish_data_record()
    