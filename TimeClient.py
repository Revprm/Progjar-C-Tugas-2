import socket, threading, time, argparse, logging

CRLF = "\r\n"
BUFFER_SZ = 1024


def worker(thread_id, host, port, rounds, delay):
    sock = socket.socket()
    try:
        sock.connect((host, port))
        logging.info(f"[T{thread_id}] Connected")
        for i in range(1, rounds + 1):
            sock.sendall(f"TIME{CRLF}".encode())
            data = sock.recv(BUFFER_SZ)
            if not data:
                break
            logging.info(f"[T{thread_id}][{i}] {data.decode().strip()}")
            time.sleep(delay)
        sock.sendall(f"QUIT{CRLF}".encode())
    except ConnectionRefusedError:
        logging.error(f"[T{thread_id}] Connection refused")
    except Exception as e:
        logging.error(f"[T{thread_id}] Error: {e}")
    finally:
        sock.close()
        logging.info(f"[T{thread_id}] Closed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=45000)
    parser.add_argument("-n", "--threads", type=int, default=3)
    parser.add_argument("-r", "--rounds", type=int, default=5)
    parser.add_argument("-d", "--delay", type=float, default=0.5)
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    threads = []
    for tid in range(1, args.threads + 1):
        t = threading.Thread(
            target=worker,
            args=(tid, args.host, args.port, args.rounds, args.delay),
            daemon=True,
        )
        threads.append(t)
        t.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        logging.warning("Interrupted by user")


if __name__ == "__main__":
    main()
