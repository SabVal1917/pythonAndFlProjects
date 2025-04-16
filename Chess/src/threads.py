#!/bin/python

import socket
import threading

class ListenerThread(threading.Thread):
    BYTES_PER_MESSAGE = 1024
    def __init__(self, name, conn):
        super().__init__()
        self.sender_name = name
        self.connection = conn
    def run(self):
        while True:
            received_message = self.connection.recv(self.BYTES_PER_MESSAGE).decode()
            print(f'{self.sender_name}: {received_message}')

class SenderThread(threading.Thread):
    def __init__(self, name, conn):
        super().__init__()
        self.sender_name = name
        self.connection = conn
    def run(self):
        while True:
            message = input()
            self.connection.send(message.encode())