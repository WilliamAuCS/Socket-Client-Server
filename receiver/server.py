import sys
import os
import socket
import argparse
import commands

def start_connection(port_number):

    # Creating new socket
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the previous socket to port port_number
    newSocket.bind(('', port_number))

    # Listen on newSocket
    newSocket.listen(1)
    return newSocket

def receive_data(sock, total_bytes):

    # Current buffer to receive
    receive_buff = ''

    # Helper buffer
    help_buff = ''

    # Continue receiving bytes until complete
    while len(receive_buff) < total_bytes:
        # Attempt to receive sent bytes
        help_buff = sock.recv(total_bytes)

        # If connection closed, break
        if not help_buff:
            break
        # Add contents of helper to main buffer
        receive_buff += help_buff
    return receive_buff

def send_data(data, sock):

    if data:
        # Convert size of data into string
        data_size_str = str(len(data))

        # If size of data is less than 10 digits, prepend 0's in header until
        # it reaches 10 digits
        while len(data_size_str) < 10:
            data_size_str = '0' + data_size_str

        # Prepend header to original data
        new_data = data_size_str + data

        # Counts number of bytes sent
        amount_sent = 0

        # Send data until complete
        while amount_sent < len(new_data):
            amount_sent += sock.send(new_data[amount_sent:])
        return amount_sent
    # If no data was received or null, return 0
    return 0

def connect_to_channel(serv_address, serv_port):

    try:
        print("Opening TCP connection for data transfer...")

        # Creating socket for TCP connection
        connection_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        connection_sock.connect((serv_address, serv_port))
        return connection_sock

    except socket.error as msg:
        print(msg)
        return connection_sock is None

def receive_client_data(sock):

    # Get header of socket
    data_buff_size = receive_data(sock, 10)

    # Check for buffer overflow
    if int(data_buff_size) > 65536:
        return None
    # Set data_size to received data size
    data_size = int(data_buff_size)

    # Retrieve data from socket
    data = receive_data(sock, data_size)
    return data;

def receive_e_port(sock, serv_address):
    port_size = 0
    port_buff_size = ''
    e_port = ''
    e_port = receive_data(sock, 5)

    print("Emphemeral port: ", e_port)
    return e_port

def main(port_num):

    newSocket = start_connection(port_num)
    print("Waiting for connection...")

    # Accept connection
    client_socket, addr = newSocket.accept()

    # Retrieve client IP
    client_addr = socket.gethostbyaddr(str(addr[0]))
    print ("Client connection accepted: ", addr)
    print ("\n")

    while True:
        # Temp buffer for command
        cmd_buff_size = ''
        # Command size
        cmd_size = 0
        # Buffer to command from client
        cmd_client = ''
        # Retrieve first 10 bytes indicating file size
        cmd_buff_size = receive_data(client_socket, 10)
        print("Size of file: ", cmd_buff_size)

        cmd_size = int(cmd_buff_size)
        print("Command size: ", cmd_size, " bytes")

        # Receive client command
        cmd_client = receive_data(client_socket, cmd_size).strip()
        print("Executing command: ", cmd_client)

        if cmd_client == 'ls':
            # Get e_port from client packet
            e_port = receive_e_port(client_socket, client_addr[0])

            # Connect to the data channel
            data_chan = connect_to_data_channel(client_addr[0], int(e_port))

            # Lines after 'ls' command
            next_str = ''
            for next in commands.getoutput('ls -l'):
                next_str += str(next)
            print(next_str)
            if send_data(next_str, data_chan):
                send_data('Server: Successfully executed command: ', client_socket)
                print("Response success...")
                print("\n")
            else:
                send_data('Server: Could not execute command: ', client_socket)
                print("Response failed")
                print("\n")
        elif cmd_client == 'quit':

            # Acknowledge client packet as response:
            send_data('Server: ack quit', client_socket)

            # Retrieve client packet
            data = receive_client_data(client_socket)
            print(data)
            break

        elif len(cmd_client) > 2:
            # Get name of file
            file_name = cmd_client[4:]
            if 'get' in cmd_client[:4]:

                # Get e_port from client packet
                e_port = recv_ephemeral_port(client_socket, client_addr[0])

                # Connect to channel
                data_chan = connect_to_data_channel(client_addr[0], int(e_port))
                print("Sending ", file_name)

                # Create file objet
                file_obj
                try:
                    file_obj = open(file_name, "rb")
                except IOError as msg:
                    send_data(str(msg), data_chan)
                    send_data(str(msg), client_socket)

                if file_obj:

                    # Retrieve size of the file
                    current_dir = os.getcwd() + '/' + file_name
                    file_size = os.path.getsize(current_dir)
                    print("Size of file: ", file_size, " bytes")

                    # Check for overflow
                    if file_size > 65536:
                        msg = "File to large"
                        if send_data(msg, data_chan):
                            print("Response Success\n")
                        else:
                            print("Response failed\n")
                        send(msg, client_socket)
                    else:

                        # Send file to client
                        file_data = file_obj.read()
                        if send_data(file_data, data_chan):
                            send_data('Server: Execution successful: ', client_socket)
                            print("Response successful")
                            print("\n")
                        else:
                            send_data('Server: Could not execute command: ', client_socket)
                            print("Response failed")
                            print("\n")
                elif 'put' in cmd_client[:4]:
                    print("Receiving file ", file_name)

                    send_data('Server: ACK, prepare to receive', client_socket)

                    # Get e_port
                    e_port = receive_client_data(client_socket)

                    data_chan = connect_to_data_channel(client_addr[0], int(e_port))

                    data = receive_client_data(data_chan)

                    if data:

                        with open(file_name, 'wb') as file_to_write:
                            file_to_write.write(data)
                            send_data('Server: Successfully executed: ', data_chan)
                            print("Success\n")

                    else:
                        print("Command could not be executed")
                        print("\n")
                        send_data('Server: Could not execute command: ', data_chan)
                        print(data)
                        print("\n")

                    data_chan.close()
                else:
                    send_data('Server: Command not found: ', client_socket)

    client_socket.close()

if __name__ == '__main__':
    psr = argparse.ArgumentParser(description='FTB Socket for Server')
    psr.add_argument('port', type=int, help='server port number', metavar='<PORT NUMBER>')
    args = psr.parse_args()
    main(args.port)
