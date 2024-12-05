# BruteForce-Camera-H.264-
BruteForce Camera H.264 

# Brute Force Script 

## Requirements

- Python 3.x
- `socket` (Standard library)
- `base64` (Standard library)
- `argparse` (Standard library)
- `os` (Standard library)
- `threading` (Standard library)


1. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. No additional dependencies are required as the script uses standard libraries.

## Usage

To run the brute-force attack, execute the script with the following parameters:

```bash
python bruteforce.py -H <target_ip> -p <target_port> -l <wordlist_file> [-t <threads>]
```

### Arguments

- `-H`, `--host`: **(Required)** Target host IP address.
- `-p`, `--port`: **(Required)** Target port number.
- `-l`, `--wordlist`: **(Required)** Path to the wordlist file (one password per line).
- `-t`, `--threads`: **(Optional)** Number of concurrent threads to use (default is 10).

### Example

```bash
python bruteforce.py -H 192.168.1.1 -p 8080 -l /path/to/wordlist.txt -t 20
```

This command will run a brute-force attack on the host `192.168.1.1` on port `8080` using 20 threads and the specified wordlist.


