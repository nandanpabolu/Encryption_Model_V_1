#!/usr/bin/env python
import sys
import time

def log_message(log_file, message):
    current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    action, msg = message.split(' ', 1)
    with open(log_file, 'a') as f:
        f.write(f"{current_time} [{action}] {msg}\n")

def main():
    log_file = sys.argv[1]  # log file is passed as argument
    print(f"Logger started, writing to {log_file}")  # Debugging print
    while True:
        try:
            message = sys.stdin.readline().strip()  # Read from stdin
            print(f"Received message: {message}")  # Debugging print
            if message == "QUIT":
                break
            log_message(log_file, message)
        except Exception as e:
            print(f"Error: {e}")  # Print any errors encountered
            break

if __name__ == "__main__":
    main()