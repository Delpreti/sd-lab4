import socket
import select
import sys
import threading

class MyServer:
    """ Classe para encapsular as funcionalidades de servidor """
    def __init__(self, hostname='', port=5000):
        self.hostname = hostname
        self.port = port
        self._internal_socket = socket.socket()
        
        self.entradas = [sys.stdin]
        self.connections = {}
        self.connections_lock = threading.Lock()

        self.method = None

        self.quit_flag = False

    def __enter__(self):
        self._internal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._internal_socket.bind((self.hostname, self.port))
        self._internal_socket.listen(5)
        self._internal_socket.setblocking(False)
        self.entradas.append(self._internal_socket)
        print(f"Server started, listening on port {self.port}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._internal_socket.close()

    def run(self):
        while not self.quit_flag:
            reciever_list, _, _ = select.select(self.entradas, [], [])
            for reciever in reciever_list:
                if reciever == self._internal_socket:
                    self._spawn_client_thread()
                elif reciever == sys.stdin:
                    self._answer_commands()

    def set_external_method(self, function):
        """ receives a function that takes a string as an argument (request), and returns a string (response) """
        self.method = function

    def _spawn_client_thread(self):
        cliente = threading.Thread(target=self._method_caller, args=self._internal_socket.accept())
        cliente.start()

    def _answer_commands(self):
        cmd = input()
        if cmd == "exit":
            if self.connections:
                print("Failed to exit the server: there are open connections")
            else: 
                self.quit_flag = True
        elif cmd == "hist":
            print(str(self.connections.values()))

    def _register_connection(self, conn, addr):
        self.connections_lock.acquire()
        self.connections[conn] = addr
        self.connections_lock.release()
        print("Accepted connection from: ", addr)

    def _unregister_connection(self, conn):
        self.connections_lock.acquire()
        del self.connections[conn]
        self.connections_lock.release()

    def _method_caller(self, conn, addr):
        self._register_connection(conn, addr)
        while True:
            data = conn.recv(1024)
            if not data:
                print(str(addr) + " has requested to end his session.")
                self._unregister_connection(conn)
                conn.close()
                return
            conn.sendall(bytes(self.method(data), 'utf-8'))

