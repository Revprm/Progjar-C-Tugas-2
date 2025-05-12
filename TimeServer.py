from socket import *
import threading
import logging
from datetime import datetime

CRLF = "\r\n"


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        super().__init__(daemon=True)
        self.connection = connection
        self.address = address

    def run(self):
        logging.info(f"[CONNECTED] {self.address}")
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                
                request = data.decode("utf-8").strip()
                # proses setiap baris yang diakhiri CRLF
                if request == "QUIT":
                    logging.info(f"Client {self.address} disconnected.")
                    break
                
                if request.startswith("TIME"):
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                else:
                    self.connection.sendall(b"Invalid request\r\n")
        except Exception as e:
            logging.error(f"Error with client {self.address}: {e}")
        finally:
            self.connection.close()


class Server(threading.Thread):
    def __init__(self, host="0.0.0.0", port=45000):
        super().__init__(daemon=True)
        self.the_clients = []
        self.my_socket = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port

    def run(self):
        self.my_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.my_socket.bind((self.host, self.port))
        self.my_socket.listen(5)
        logging.warning(f"[STARTED] Time server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.my_socket.accept()
            logging.warning(f"Connection from {addr}")
            clt = ProcessTheClient(conn, addr)
            clt.start()
            self.the_clients.append(clt)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    svr = Server()
    svr.start()
    # biarkan main thread hidup
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        logging.warning("\n[SHUTDOWN] Server is shutting down.")


if __name__ == "__main__":
    main()