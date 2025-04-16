#!/bin/python

import abc
import os
import socket
import time
from threading import Thread

from server import Server
from src.client import Client
from src.coder import Coder

PORT = 10000

def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        sock.connect(("10.255.255.255", 1))
        ip = sock.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        sock.close()
    return ip

class ConsoleLauncher:
    def __init__(self):
        self.handler = None
        self.input_listener = None
        self.server = None
        self.client = None
        pass

    def start(self):
        self.input_listener = self.InputListener()
        self.start_handler(self.MenuHandler)
        self.input_listener.start()
        self.input_listener.join()

    def __del__(self):
        try:
            self.client.close(0)
            print(1)
        except:
            pass
        try:
            if self.server:
                self.server.close()
        except:
            pass
        try:
            self.input_listener.stop()
        except:
            pass

    def start_server(self):
        addr = (get_ip(), PORT)
        self.server = self.ServerThread(addr)
        self.server.start()
        time.sleep(1)
        self.start_client(addr)
        self.handler.display("Server started", f"{addr[0]}:{addr[1]}")
        self.server.join()
        pass

    def start_client(self, addr):
        self.client = Client(addr, self)
        pass

    def start_handler(self, handler):
        self.handler = handler(self)
        self.input_listener.bind(self.handler)

    def receive(self, data):
        self.handler.receive(data)

    def on_enter(self, inp):
        self.client.send(inp)

    def catch_closing(self, code):
        if code == 0:
            # Game ended normally
            self.start_handler(self.EndHandler)
        elif code == 1:
            # Server was closed
            print("Server was closed")

    class ServerThread(Thread):
        def __init__(self, addr):
            super().__init__()
            self.daemon = True
            self.addr = addr

        def run(self):
            self.server = Server(self.addr)

        def stop(self):
            self.server.close()

    class InputListener(Thread):
        def __init__(self):
            super().__init__()
            self.daemon = True
            self.handler = None
            self.active = True

        def bind(self, handler):
            self.handler = handler

        def run(self):
            while self.active:
                inp = input()
                self.handler.parse(inp)

        def stop(self):
            print("1 should stop")
            self.active = False

    class CommonHandler:
        def __init__(self, launcher):
            self.launcher = launcher

        @abc.abstractmethod
        def parse(self, inp):
            pass

        @abc.abstractmethod
        def receive(self, data):
            pass

        @abc.abstractmethod
        def display(self, data):
            pass

    class MenuHandler(CommonHandler):
        def __init__(self, launcher):
            super().__init__(launcher)
            self.asked = "connection"
            self.ask(self.asked)

        def ask(self, request):
            if request == "connection":
                self.display("Choose the type of connection (server/client): ")
            elif request == "address":
                self.display("Enter the address of the server (ip:host): ")

        def parse(self, inp):
            if self.asked == "connection":
                if inp in ("server", "s", "1"):
                    self.launcher.start_server()
                    self.asked = "nothing"
                elif inp in ("client", "c", "2"):
                    self.asked = "address"
                    self.ask(self.asked)
            elif self.asked == "address":
                try:
                    ip, port = inp.split(":")
                    self.launcher.start_client((ip, int(port)))
                    self.asked = "nothing"
                except Exception as e:
                    self.display("Some error occurred:\n", e)

        def display(self, *args):
            print(*args)

        def receive(self, data):
            code, data = data.split("|")

            if data == "lobby's assembled":
                self.on_lobby_assembled()
                return
            self.display(data)

        def on_lobby_assembled(self):
            self.display("Lobby's assembled. Starting game")
            time.sleep(1)
            self.launcher.start_handler(self.launcher.InGameHandler)

    class InGameHandler(CommonHandler):
        def __init__(self, launcher):
            super().__init__(launcher)

        def parse(self, inp):
            # parse user input
            self.launcher.on_enter(inp)

        def display(self, *args):
            os.system("clear")
            print(*args)

        def on_game_end(self, out):
            self.display(out)
            self.launcher.start_handler(self.launcher.EndHandler)

        def receive(self, data):
            code = data.split("|")[0]
            if code == "end":
                fen = data.split("|")[1]
                board = Coder.decode(fen)
                text = data.split("|")[2]
                self.on_game_end(board + text)
            elif code == "active":
                fen = data.split("|")[1]
                board = Coder.decode(fen)
                text = data.split("|")[2]
                self.display(board + text)

    class EndHandler(CommonHandler):
        def __init__(self, launcher):
            super().__init__(launcher)
            self.display("SOME RANDOM TEXT TO BE CHANGED")  # CHANGE

        def parse(self, inp):
            pass

        def display(self, *args):
            os.system("clear")
            print(*args)
            print("To end game press ENTER")

        def receive(self, data):
            pass
