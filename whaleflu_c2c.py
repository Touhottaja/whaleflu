#!/usr/bin/python3
import socket

C2C_HOST = "192.168.0.1"
C2C_PORT = 4000


def main() -> None:
    s = socket.socket()
    try:
        s.bind((C2C_HOST, C2C_PORT))
    except socket.error as e:
        print(f"Failed to bind to {C2C_HOST}:{C2C_PORT}: {e}")
        return

    print("C2C listening for connections...")
    s.listen(1)

    while True:
        try:
            c, addr = s.accept()
            print(f"Connection accepted from {addr}")

            while True:
                data = c.recv(1024)
                if not data:
                    break
                print(data)

                response = b"OK"
                c.send(response)

        except socket.error as e:
            print(f"Socket error: {e}")

        finally:
            c.close()


if __name__ == "__main__":
    main()
