#!/usr/bin/python3
import socket

C2C_HOST = "192.168.0.1"
C2C_PORT = 4000


def main() -> None:
    s = socket.socket()
    s.bind((C2C_HOST, C2C_PORT))

    print("C2C listening for connections...")
    s.listen(1)
    c, addr = s.accept()
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data)

        data = b"OK"
        c.send(data)

    c.close()


if __name__ == "__main__":
    main()
