import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 45000
BUFFER_SIZE = 1024
CRLF = "\r\n"


class ClientHandler(threading.Thread):
    """Thread untuk menangani koneksi satu client."""

    def __init__(self, conn: socket.socket, addr: tuple[str, int]):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self._buffer = ""

    def run(self):
        print(f"[CONNECTED] {self.addr}")
        try:
            while data := self.conn.recv(BUFFER_SIZE):
                self._buffer += data.decode("utf-8", errors="ignore")
                while CRLF in self._buffer:
                    line, self._buffer = self._buffer.split(CRLF, 1)
                    self._handle_command(line.strip())
        finally:
            self.conn.close()
            print(f"[DISCONNECTED] {self.addr}")

    def _handle_command(self, cmd: str):
        cmd_upper = cmd.upper()
        match cmd_upper:
            case "TIME":
                now = datetime.now().strftime("%d %m %Y %H:%M:%S")
                response = f"JAM {now}{CRLF}"
                self.conn.sendall(response.encode("utf-8"))
                print(f"[SENT] {self.addr} -> {response.strip()}")
            case "QUIT":
                print(f"[QUIT] {self.addr}")
                self.conn.close()
                # menghentikan thread
                raise SystemExit
            case _:
                err = f"ERROR Unknown command{CRLF}"
                self.conn.sendall(err.encode("utf-8"))


def start_server():
    """Inisialisasi dan loop utama server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"[STARTED] Time server listening on {HOST}:{PORT}")

        try:
            while True:
                conn, addr = srv.accept()
                handler = ClientHandler(conn, addr)
                handler.start()
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Server is shutting down.")


if __name__ == "__main__":
    start_server()
