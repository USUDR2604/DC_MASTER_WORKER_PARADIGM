from xmlrpc.server import SimpleXMLRPCServer
import sys
import json
import random

data_table = {}

def load_data(group):
    filename = f"data-{group}.json"
    try:
        with open(filename, 'r') as file:
            data_table.update(json.load(file))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{filename}'.")
        sys.exit(1)

## Getting Details via name from records
def get_by_name(name):
    try:
        result = [data for data in data_table.values() if data['name'] == name]
        return {'error': False, 'result': result}
    except Exception as e:
        return {'error': True, 'message': str(e)}

## getting details via location from records
def get_by_location(location):
    try:
        result = [data for data in data_table.values() if data['location'] == location]
        return {'error': False, 'result': result}
    except Exception as e:
        return {'error': True, 'message': str(e)}

## getting details via location and year
def get_by_year(location, year):
    try:
        result = [data for data in data_table.values() if data['location'] == location and data['year'] == year]
        return {'error': False, 'result': result}
    except Exception as e:
        return {'error': True, 'message': str(e)}

## Get Details by Only year
def get_details_by_year(year):
    try:
        result = [data for data in data_table.values() if data['year'] == year]
        return {'error': False, 'result': result}
    except Exception as e:
        return {'error': True, 'message': str(e)}

## Publishing data to records
def publish_data(data):
    try:
        data_id = len(data_table) + 1
        data_table[data_id] = data
        print(f"Data published: {data}")
        return {'error': False, 'message': f"Data published with ID: {data_id}"}
    except Exception as e:
        return {'error': True, 'message': str(e)}

def main():
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        group = sys.argv[2]
    except ValueError:
        print("Error: Invalid port number.")
        sys.exit(1)

    load_data(group)

    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")
    ### Registering Functions on servers
    server.register_function(get_by_name, 'getbyname')
    server.register_function(get_by_location, 'getbylocation')
    server.register_function(get_by_year, 'getbyyear')
    server.register_function(publish_data, 'publish_data')
    server.register_function(get_details_by_year,'getdetailsbyyear')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server terminated by user.")

if __name__ == '__main__':
    main()
