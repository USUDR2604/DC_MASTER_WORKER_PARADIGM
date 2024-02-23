import xmlrpc.client
import sys

try:
    master_port = int(sys.argv[1])
except IndexError:
    print("Error: Please provide the master port as a command line argument.")
    sys.exit(1)
except ValueError:
    print("Error: The master port must be an integer.")
    sys.exit(1)

try:
    with xmlrpc.client.ServerProxy(f"http://localhost:{master_port}/") as proxy:
        name = 'uday'
        print(f'Client => Asking for person with {name}')
        result = proxy.getbyname(name)
        print(f"Server => finding details with name {name}")
        if not result['error']:
            print(f"{len(result['result'])} Records found")
            for val in result['result']:
                print(f"Server => {val['name']} located at {val['location']}")
            print(result['result'])
            print()
        else:
            print(f"Server =>Oops! No data Record Found")
            print()

        location = 'Kansas City'
        print(f'Client => Asking for person lived at {location}')
        result = proxy.getbylocation(location)
        print(f"Server => finding details about who lived at {location}")
        if not result['error']:
            print(f"{len(result['result'])} Records found")
            for val in result['result']:
                print(f"Server => {val['name']} located at {val['location']}")
            print(result['result'])
            print()
        else:
            print(f"Server =>Oops! No data Record Found")
            print()

        location = 'New York City'
        year = 2002
        print(f'Client => Asking for person lived in {location} in {year}')
        result = proxy.getbyyear(location, year)
        print(f"Server => finding details related to this {location} location in {year}")
        if not result['error']:
            print(f"{len(result['result'])} Records found")
            for val in result['result']:
                print(f"Server => {val['name']} located at {val['location']} in {val['year']}")
            print(result['result'])
            print()
        else:
            print(f"Server =>Oops! No data Record Found")
            print()

except ConnectionError:
    print("Error: Unable to connect to the server. Please make sure the server is running.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
