import sys
import os
import socket
import argparse
import commands

def start_connection():
    try:
        # Creating the socket
        startSocket = socket.socket(socket.AF_INIT, socet.SOCK_STREAM)

        startSocket.bind(('', 0))

        startSocket.listen(1)
        return startSocket

    # If error occurs
    except socket.error as msg:
        print "Socket Error: ", msg
        return startSocket is None

def create_connection(serverIP, serverPort):
    # Establishes connection to control channel to send commands to server

    try:
        # Creating the TPC socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((serverIP, serverPort))
        return sock

    # If error occurs
    except:
        socket.error as msg:
        print "Socket Error: ", msg
        return sock is None

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
        print "Sending packet... ", client_send_data

        # Amount of bytes sent
        sentCount = 0

        # Sending data
        while sentCount < data_size_len:
            sentCount += sock.send(nData[sentCount:])
        print sentCount, " bytes sent... "
        return sentCount

    # If data is empty or null
    return 0
