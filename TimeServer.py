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
        self.buffer = ""

    def run(self):
        logging.info(f"[CONNECTED] {self.address}")
        try:
            while True:
                data = self.connection.recv(32)
                if not data:
                    break
                # decode dan tambahkan ke buffer
                self.buffer += data.decode("utf-8", errors="ignore")
                # proses setiap baris yang diakhiri CRLF
                while CRLF in self.buffer:
                    line, self.buffer = self.buffer.split(CRLF, 1)
                    cmd = line.strip().upper()
                    if cmd == "QUIT":
                        logging.info(f"[QUIT]     {self.address}")
                        return  # keluar thread, koneksi ditutup di finally
                    elif cmd == "TIME":
                        now = datetime.now().strftime("%H:%M:%S")
                        response = f"JAM {now}{CRLF}"
                        self.connection.sendall(response.encode("utf-8"))
                        logging.info(f"[SENT]     {self.address} -> {response.strip()}")
                    else:
                        err = f"ERROR Unknown command{CRLF}"
                        self.connection.sendall(err.encode("utf-8"))
        finally:
            self.connection.close()
            logging.info(f"[DISCONNECTED] {self.address}")


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
