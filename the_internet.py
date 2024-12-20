"""
File:        the_internet.py
Author:      Freeman Addo
Date:        12/4/2024
Section:     11
E-mail:      faddo1@umbc.edu
Description: Run the internet in python
"""

def create_server(servers, server_name, ip):
    for existing_servers in servers: 
        # Checks if any existing server has the same IP address as the new server or if there is a duplicate
        if servers[existing_servers] == ip:
            return servers # If there is a duplicate it returns the servers dictionary without any changes
        
    servers[server_name] = ip # If no matching IP is found, add the new server to the 'servers' dictionary
    print(f'Success: A server with name {server_name} was created at ip {ip}') # Prints a success message for making a new server
    return servers # Prints the updated servers dictionary


def create_connection(servers, connections, server1, server2, connection_time):
    if server1 not in servers or server2 not in servers: # Checks if either server is in the servers dictoinary
        print("There has been an issue.")
        return connections # If neither are found it prints out the follong message and returns the unchanged connections dictionary
    
    if (server1, server2) in connections or (server2, server1) in connections:
        print(f"{server1} and {server2} are already connected.")
        return connections
    
    connection_key = (server1, server2) # A key is created for the connection using the server names
    connections[connection_key] = connection_time # Adds the connection to the connection dictionary with the specified connection time
    print(f'Success: A server with name {server1} is now connected to {server2}')
    return connections # Prints out the success message and and prints the updated connections dictionary


def set_server(servers, current_server, identified_server):
     if identified_server in servers: # Checks if the identified server is in the servers dictionary
        current_server = identified_server # If found, updates the current server to the found identified server
        print(f"Server {identified_server} selected.")
        return current_server # Prints message and returns the updated current server
     
     print(f"Server or IP address {identified_server} not found.") # Prints out error message if it's not found
     return current_server # Returns current server without any changes


def ip_config(servers, current_server):
    if current_server is None: # Checks if there is no server set
        print("No server is set.") # If no server is set this message prints.
    else:
        print(f"{current_server}    {servers[current_server]}") # If the server is set, it prints out the associated server and ip address


def display_servers(servers, connections):
    for server in servers: # Goes through each server in the servers dictionary
        print(f"\t{server}    {servers[server]}") # Prints servers name and associated ip address

        connected_servers = [] # All of the connected servers are stored here

        
        for connection in connections: # Goes through connections to find which ones are involved with the current server
            server1, server2 = connection  # Unpacks the connections into servers and the connection time
            time = connections[connection]  

            # Check if the current server is either server1 or server2 in the connection
            if server1 == server: 
                connected_servers.append((server2, time)) # If so, add the connected server (server2) and the connection time to the list
            elif server2 == server:
                connected_servers.append((server1, time))  # If the current server is server2, add server1 and the connection time to the list

        
        for connected_server, time in connected_servers: # Goes through the list of each connected server and prints them
            print(f"\t\t{connected_server}    {servers[connected_server]}    {time}")


def ping(servers, connections, current_server, target, visited=None, total_time=0):

    if visited is None:
        visited = []  

    # Makes the target servers name equal to the target server (for ip to server name conversion)
    target_server_name = target 

    # Find the server name corresponding to the IP address of the target and displays it
    for server_name in servers:  
        if servers[server_name] == target: 
            target_server_name = server_name  

     # If the current server is the target, or the current server's IP matches the target's IP
    if current_server == target_server_name or servers[current_server] == target:
        # Print the reply message and total time taken
        print(f"Reply from {servers[target_server_name]}  time = {total_time} ms")
        return True

    # If the current server has been visited the recursion stops
    if current_server in visited:
        return False
            

    # Marks the current server as visited
    visited.append(current_server)  

    # Goes through different connections to see which ones are connected to the current server
    for connection in connections:  
        server1, server2 = connection  
        time = connections[connection]  

        # If current server is 'server1' and 'server2' has not been visited
        if server1 == current_server and server2 not in visited:
            new_time = total_time + time  # Add the connection time to the total time
            if ping(servers, connections, server2, target, visited, new_time): # Pings the next server
                return True # If the target is found, it returns true
            
            # Returns the if statement but vice versa
        elif server2 == current_server and server1 not in visited:
            new_time = total_time + time  
            if ping(servers, connections, server1, target, visited, new_time):
                return True 
            
    return False # Return False if no path to the target server is found


def traceroute(servers, connections, current_server, target_server, visited=None, hop_count=0):

    if visited is None:
        visited = []  

    # If no server is set, print an error message and return False
    if current_server is None:
        print("No server is set.")
        return False
    
    # If the current server has already been visited, stop the recursion
    if current_server in visited:
        return False
    
    # Makes the target servers name equal to the target server (for ip to server name conversion)
    target_server_name = target_server  

    # Find the server name corresponding to the IP address of the target and displays it
    for server_name in servers:  
        if servers[server_name] == target_server: 
            target_server_name = server_name  
            
    # If the current server is the target, or its IP matches the target's IP, the message is printed and it returns true
    if current_server == target_server or servers[current_server] == target_server:
        print("Trace complete.")
        return True

    # Marks the current server as visited
    visited.append(current_server)

    # Prints the first hop starting from the current server
    if hop_count == 0:
        print(f"Tracing route to {target_server_name} [{target_server}]")
        print(f" {hop_count}    0    [{servers[current_server]}]    {current_server}")

     # Find the connected servers that haven't been visited yet
    connected_servers = []
    for connection in connections:  
        server1, server2 = connection  
        time = connections[connection]  # Get the connection time for the pair

        # If server1 is the current server, add server2 to the list of connected servers and vice versa
        if server1 == current_server and server2 not in visited:
            connected_servers.append((server2, time))
        elif server2 == current_server and server1 not in visited:
            connected_servers.append((server1, time))

     # If there are no connected servers, stop the trace and return False
    if not connected_servers:
        return False

    # Recursively traces through the path through each  connected servers
    for connected_server, time in connected_servers:
        hop_count += 1  # Increments the hop
        print(f" {hop_count}    {time}    [{servers[connected_server]}]    {connected_server}") # Prints the current hop details

        # Recursively traces path to the target server
        if traceroute(servers, connections, connected_server, target_server, visited, hop_count): 
            return True # If the target server is found return true  

    return False # If the target cannot be reached, return False


def run_the_internet():

    # Dictionaries made for severs, connections, and a variable for current server
    servers = {}
    connections = {}
    current_server = None

    disconnect_internet = False # Flag for exiting the program

    while not disconnect_internet:
        command = input(">>> ") # Prompts the user for a command

        # If the user inputs nothing and presses enter, nothing happens and the program continues

        # Exits the program when the user enters 'quit'
        if command.strip():
            if command == 'quit':
                disconnect_internet = True

            # Splits the command into parts
            server_and_ip = command.split()

            # If the command is 'create-server', create a new server
            if len(server_and_ip) == 3 and server_and_ip[0] == 'create-server':
                server_name = server_and_ip[1]
                ip = server_and_ip[2]
                servers = create_server(servers, server_name, ip)
            
            # If the command is 'create-connection', create a new connection between two servers
            elif len(server_and_ip) == 4 and server_and_ip[0] == 'create-connection':
                server1 = server_and_ip[1]
                server2 = server_and_ip[2]
                connection_time = int(server_and_ip[3])
                connections = create_connection(servers, connections, server1, server2, connection_time)
            
            # If the command is 'set-server', set the current server to the one specified by the user
            elif len(server_and_ip) == 2 and server_and_ip[0] == 'set-server':
                identified_server = server_and_ip[1]
                current_server = set_server(servers, current_server, identified_server)

            # If the command is 'traceroute' or 'tracert', perform a traceroute to the target server
            elif len(server_and_ip) == 2 and server_and_ip[0] == 'traceroute' or server_and_ip[0] == 'tracert':
                target_server = server_and_ip[1]
                if current_server is None:
                    print("No server is set.") # Prints an error message if the server isn't set
                else:
                    destination_found = False
                    # Check if the target server exists in the connections
                    for connection in connections:  
                        server1, server2 = connection  
                        if server1 == target_server or server2 == target_server or servers[server1] == target_server or servers[server2] == target_server:
                            destination_found = True
                            
                    # If the target server cannot be reached, print an error message
                    if not destination_found:
                        print(f"Unable to route to target system name {target_server}.")
                    else:
                        if not traceroute(servers, connections, current_server, target_server, visited=[]):
                            print(f"Unable to route to target system name {target_server}.")

            # If the command is 'ping', send a ping to the target server and display it
            elif len(server_and_ip) == 2 and server_and_ip[0] == 'ping':
                target = server_and_ip[1]
                if current_server is None:
                    print("No server is set.") # Prints an error message if the server isn't set

                else:
                    destination_found = False
                    # Check if the target server exists in the connections
                    for connection in connections:  
                        server1, server2 = connection  
                        if server1 == target or server2 == target or servers[server1] == target or servers[server2] == target:
                            destination_found = True
                            
                    # If the target server cannot be pinged, print an error message
                    if not destination_found:
                        print(f"Unable to ping target system name {target}.")
                    else:
                        if not ping(servers, connections, current_server, target, visited=[]):
                            print(f"Unable to ping target system name {target}.")

            # If the command is 'ip-config', show the current server's IP configuration
            elif len(server_and_ip) == 1 and server_and_ip[0] == 'ip-config':
                ip_config(servers, current_server)

            # If the command is 'display-servers', display all the servers and their connections
            elif command == 'display-servers':
                display_servers(servers, connections)  

# Run the 'run_the_internet' function if this script is executed directly
if __name__ == '__main__':
    run_the_internet()