#!/bin/python

import socket
from threading import Thread

class Client:
    def __init__(self, address, owner):
        self.owner = owner

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)

        self.listener = self.ListenerThread(self.sock, self)
        self.listener.start()

    def __del__(self):
        self.sock.close()

    def send(self, data):
        self.sock.send(data.encode())

    def receive(self, data):
        if data == "":
            print("Server was closed, disconnecting")
            self.close(0)
        else:
            self.owner.receive(data)

    def close(self, code):
        self.listener.stop()
        self.sock.close()
        self.owner.catch_closing(code)
        print(1)
        try:
            self.listener.join()
        except:
            pass

    class ListenerThread(Thread):
        BYTES_PER_MESSAGE = 1024

        def __init__(self, conn, client):
            super().__init__()
            self.daemon = True
            self.conn = conn
            self.client = client
            self.active = True

        def run(self):
            try:
                while self.active:
                    data = self.conn.recv(self.BYTES_PER_MESSAGE).decode()
                    self.client.receive(data)
            except ConnectionResetError:
                print("Connection closed")
                raise

        def stop(self):
            self.active = False
