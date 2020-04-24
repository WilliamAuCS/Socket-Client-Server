import sys
import os
import socket
import argparse
import commands

def create_connection(serverIP, serverPort):
    # Establishes connection to control channel to send commands to server

    try:
        # Creating the TPC socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((serverIP, serverPort))
        return sock

    # If error occurs
    except socket.error as msg:
        print ("Socket Error: ", msg)
        return sock is None


def start_connection():
    try:
        # Creating the socket
        startSocket = socket.socket(socket.AF_INIT, socet.SOCK_STREAM)

        startSocket.bind(('', 0))

        startSocket.listen(1)
        return startSocket

    # If error occurs
    except socket.error as msg:
        print ("Socket Error: ", msg)
        return startSocket is None


def client_send_data(sock, data, sock_data = None):

    if data:
        # Length of data in string format
        data_size = str(len(data))

        # Holding size of data_size
        data_size_len = len(data_size)

        # Create header indicating data data size
        # If size is less than given size, prepend 0's
        while data_size_len < 10:
            data_size = '0' + data_size

        # Add previously created header to front of string
        nData = data_size + data
        data_size_len = len(nData)

        if any(cmd in data for cmd in ['get', 'insert', 'ls']) and sock_data:
            nData += str(sock_data.getsockname()[1])
        print ("Sending packet... ", client_send_data)

        # Amount of bytes sent
        sentCount = 0

        # Sending data
        while sentCount < data_size_len:
            sentCount += sock.send(nData[sentCount:])
        print (sentCount, " bytes sent... ")
        return sentCount

    # If data is empty or null
    return 0

def accept_pkt(sock, num_of_bytes):

    # Buffer
    accBuff = ''
    # Buffer helper
    helpBuff = ''

    while len(accBuff) < num_of_bytes:
        # Store bytes in helper buffer
        helpBuff = sock.recv(num_of_bytes)

        #In case socket has been closed
        if not tempBuff:
            break;

        # Add bytes from helper to buffer
        accBuff += helpBuff
    return accBuff

def transfer_data(sock_control, user_input):

    print ("Opening tcp connection for data transfer...")

    # Opening connection
    connect = create_connection()

    # Displaing commands to server
    cmdSent = send(user_input, sock_control, connect)

    sock_data, ipr = data_channel.accept()

    # Size of current packet
    buff_data_size = recvAll(sock_data, 10)
    data_size = int(buff_data_size)

    # Recieve server data
    data = recvAll(sock_data, data_size)
    data_channel.close()
    print ("Closing tcp connection...")
    return data

def control_to_recv(sock_control):
    # 10 = including header
    buff_data_size = recvAll(sock_control, 10)
    data_size = int(buff_data_size)
    # Storing data
    data = recvAll(sock_control, data_size)
    return data

def main(host, port_number):
    # Establish control connection
    control_chan = start_connection(host, port_number)

    if control_chan:
        # Accept connection
        while True:
            print ('\n')
            # Take in user input
            user_input = raw_input("ftp> ").strip()

            if user_input == 'ls':
                data = transfer_data(user_input, control_chan)
                server_info = control_to_recv(control_chan)
                print (server_info)
                print ("\n")
                print ("Files on server: ")
                print ("\n")
                print (data)

            elif user_input == "quit":
                number_sent = send(user_input, control_chan)

                data = control_to_recv(control_chan)
                print (data_size)

                number_sent = send("quit successfully", control_chan)
                break

            elif len(user_input) > 2:
                # Store name of file
                file_name = user_input[4:].strip()

                if 'get' in user_input[4:]:
                    data = transfer_data(user_input, control_chan)

                    if not 'Errno' in data:

                        with open(file_name, 'wb') as write_file:
                            write_file.write(data)

                    # Display status or error from the server
                    server_info = control_to_recv(control_chan)
                    print (server_info)

                # Send file to server
            elif 'put' in user_input[4:]:
                # See if file is already opened
                try:
                    file_d = open(file_name, "rb")
                except IOError as msg:
                    print (msg)
                    continue

                # Finding size of file to be sent
                dir_d = os.getcwd() + '/' + file_name
                sent_d_size = os.path.getsize(dir_d)
                print ("Size of file to be sent: ", sent_d_size, " bytes")

                # Check for buffer overflow
                if sent_d_size > 65536:
                    print ("File too large.")
                    print ("Max file size: 65536 bytes")

                else:
                    send(user_input, control_chan)
                    server_info = control_to_recv(control_chan)
                    print (server_info)
                    print ("tcp connection open for data transfer...")

                    data_channel = create_connection()
                    eph_port = data.channel.getsocketname()[1]
                    send(str(eph_port), control_chan)
                    sock_data, ipr = data_channel.accept()

                    # Upload file
                    if sock_data:
                        f_data = file_d.read()
                        send(f_data, sock_data)
                    data_channel.close()

        # If given an unknown command, continue to send to server
        else:
            send(user_input, control_chan)
            server_info = control_to_recv(control_chan)
            print (server_info)
    control_chan.close()

if __name__ == '__main__':
    psr = argparse.ArgumentParser(description='FTB Socket for Client')
    psr.add_argument('host', type=str, help='domain name of server', metavar='<server machine>')
    psr.add_argument('port', type=int, help='server port number', metavar='<server port>')
    args = psr.parse_args()
    main(args.host, args.port)
