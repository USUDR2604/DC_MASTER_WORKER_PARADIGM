from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
import random

workers = {
    'worker-1': ServerProxy("http://localhost:23001/"),
    'worker-2': ServerProxy("http://localhost:23002/")
}

# Registering workers with their proxies
def register_worker(worker_name, worker_proxy):
    try:
        workers[worker_name] = worker_proxy
        print(f"Worker {worker_name} registered successfully.")
    except Exception as e:
        print(f"Error registering worker {worker_name}: {e}")

## Detail Extraction from db according to its location
def get_by_location(location):
    try:
        result_worker1 = workers['worker-1'].getbylocation(location)
        result_worker2 = workers['worker-2'].getbylocation(location)
        return {
            'error': False,
            'result': result_worker1['result'] + result_worker2['result']
        }
    except Exception as e:
        return {'error': True, 'message': str(e)}

##Detail Extraction from db according to name
def get_by_name(name):
    try:
        worker_key = 'worker-1' if name[0] <= 'm' else 'worker-2'
        result_worker = workers[worker_key].getbyname(name)
        return {
            'error': False,
            'result': result_worker['result']
        }
    except Exception as e:
        return {'error': True, 'message': str(e)}

## Detail Extraction from db according to its year and location
def get_by_year(location, year):
    try:
        result_worker_1 = workers['worker-1'].getbyyear(location, year)
        result_worker_2 = workers['worker-2'].getbyyear(location, year)
        return {
            'error': False,
            'result': result_worker_1['result'] + result_worker_2['result']
        }
    except Exception as e:
        return {'error': True, 'message': str(e)}

### Random Publish Data to data records 
def random_publish_data():
    try:
        data = {
            'name': f'Person-{random.randint(1, 100)}',
            'location': random.choice(['Kansas City', 'New York City', 'Los Angeles']),
            'year': random.randint(2000, 2022)
        }
        worker_key = random.choice(list(workers.keys()))
        workers[worker_key].publish_data(data)
        print(f"Random data published to {worker_key}.")
    except Exception as e:
        print(f"Error publishing random data: {e}")

def main():
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Error: Invalid port number.")
        sys.exit(1)

    try:
        server = SimpleXMLRPCServer(("localhost", port))
        print(f"Listening on port {port}...")
        ### Registering Functions in Server 
        server.register_function(register_worker, 'register_worker')
        server.register_function(get_by_location, 'getbylocation')
        server.register_function(get_by_name, 'getbyname')
        server.register_function(get_by_year, 'getbyyear')
        server.register_function(random_publish_data, 'random_publish_data')

        server.serve_forever()
        
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    main()
