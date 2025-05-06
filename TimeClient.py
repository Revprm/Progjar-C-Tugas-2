#!/usr/bin/env python3
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 45000
CRLF = "\r\n"
BUFFER_SZ = 1024


def worker(thread_id: int, rounds: int = 10, delay: float = 0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print(f"[Thread-{thread_id}] Connected to {HOST}:{PORT}")

            for i in range(1, rounds + 1):
                # Kirim TIME
                sock.sendall(("TIME" + CRLF).encode("utf-8"))
                data = sock.recv(BUFFER_SZ)
                if not data:
                    print(
                        f"[Thread-{thread_id}] Server closed connection unexpectedly."
                    )
                    return
                print(f"[Thread-{thread_id}][{i:02d}] {data.decode('utf-8').strip()}")
                time.sleep(delay)

            # Kirim QUIT
            sock.sendall(("QUIT" + CRLF).encode("utf-8"))
            print(f"[Thread-{thread_id}] Sent QUIT, closing.")
    except Exception as e:
        print(f"[Thread-{thread_id}][ERROR] {e}")


def main(num_threads: int = 5, rounds: int = 10):
    threads = []
    for tid in range(1, num_threads + 1):
        t = threading.Thread(target=worker, args=(tid, rounds), daemon=True)
        threads.append(t)
        t.start()

    # Tunggu semua selesai
    for t in threads:
        t.join()

    print("All threads finished.")


if __name__ == "__main__":
    # Contoh: 5 thread, 10 request TIME per thread
    main(num_threads=3, rounds=5)
