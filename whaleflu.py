#!/usr/bin/python3
import socket
import time

C2C_HOST = "192.168.0.1"
C2C_PORT = 4000


def main() -> None:
    s = socket.socket()
    s.connect((C2C_HOST, C2C_PORT))
    message = b"Hello, World!"

    while True:
        s.send(message)
        data = s.recv(1024)
        time.sleep(1)

    s.close()


if __name__ == "__main__":
    main()
