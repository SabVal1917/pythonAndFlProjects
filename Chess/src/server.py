#!/bin/python

import socket
from src.Game import Game
from threading import Thread

class Server:
    def __init__(self, addr):
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen()

        self.connections = []
        self.listeners = []

        self.wait_for_connections()

        self.game = Game(self)

    def __del__(self):
        for lis in self.listeners:
            lis.stop()
        self.sock.close()

    def wait_for_connections(self):
        self.connections.append(self.sock.accept())
        self.send("conn 1", "idle")
        self.connections.append(self.sock.accept())
        self.send("conn 2", "idle")

        for conn in self.connections:
            self.listeners.append(self.ListenerThread(conn[0], self))
            self.listeners[-1].start()

        self.send("lobby's assembled", "idle")

    def receive_from_player(self, data):

        self.game.input_data(data)

    def receive_from_game(self, data, code, players="all"):
        if players == "all":
            self.send(data, code)
        elif players == "first":
            self.send(data, code, (0,))
        elif players == "second":
            self.send(data, code, (1,))

    def send(self, data, code, chosen_connections=()):
        if chosen_connections == ():
            for (conn, addr) in self.connections:
                conn.send((f"{code}|" + data).encode())
        else:
            for i in chosen_connections:
                self.connections[i][0].send((f"{code}|" + data).encode())

    def close(self):
        for lis in self.listeners:
            lis.stop()
            lis.join()
        self.sock.close()

    class ListenerThread(Thread):
        BYTES_PER_MESSAGE = 1024

        def __init__(self, conn, server):
            super().__init__()
            self.conn = conn
            self.server = server
            self.active = True

        def run(self):
            while self.active:
                data = self.conn.recv(self.BYTES_PER_MESSAGE).decode()
                self.server.receive_from_player(data)

        def stop(self):
            self.active = False
