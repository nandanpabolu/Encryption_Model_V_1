#!/usr/bin/env python
import subprocess
import sys

def run_logger(log_file):
    return subprocess.Popen(['python3', 'logger.py', log_file], stdin=subprocess.PIPE, text=True)

def run_encryption():
    return subprocess.Popen(['python3', 'encryption.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

def log(logger_proc, action, message):
    if logger_proc.poll() is None:  # Check if the logger process is still running
        try:
            logger_proc.stdin.write(f"{action} {message}\n")
            logger_proc.stdin.flush()
        except BrokenPipeError:
            print("Logger process is not accepting input (broken pipe).")
            sys.exit(1)
    else:
        print("Logger process has terminated unexpectedly.")
        sys.exit(1)

def send_encryption_command(enc_proc, command):
    enc_proc.stdin.write(command + "\n")
    enc_proc.stdin.flush()
    return enc_proc.stdout.readline().strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python driver.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    
    # Start logger and encryption processes
    logger_proc = run_logger(log_file)
    enc_proc = run_encryption()

    # History will now store tuples (type, string)
    history = []  # [(type, string), ...]

    log(logger_proc, "START", "Driver program started")

    while True:
        print("Menu:")
        print("1. Set password (passkey)")
        print("2. Encrypt a string")
        print("3. Decrypt a string")
        print("4. Show history")
        print("5. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            password = input("Enter a new password: ")
            send_encryption_command(enc_proc, f"PASSKEY {password}")
            log(logger_proc, "PASSKEY", "Password set")

        elif choice == "2":
            print("1. Enter a new string")
            print("2. Select from history")
            option = input("Choose an option: ")
            if option == "1":
                text = input("Enter a string to encrypt: ")
                result = send_encryption_command(enc_proc, f"ENCRYPT {text}")
                print(result)
                if result.startswith("RESULT"):
                    encrypted_string = result.split(' ', 1)[1]
                    history.append(('plain', text))  # Store the plaintext
                    history.append(('encrypted', encrypted_string))  # Store the encrypted string
                log(logger_proc, "ENCRYPT", text)
            elif option == "2":
                # Filter history to show only plaintext
                plain_texts = [item for item in history if item[0] == 'plain']
                if not plain_texts:
                    print("No plaintext available in history.")
                    continue
                for idx, item in enumerate(plain_texts):
                    print(f"{idx+1}. {item[1]}")
                selection = int(input("Select a string from history: ")) - 1
                text = plain_texts[selection][1]
                result = send_encryption_command(enc_proc, f"ENCRYPT {text}")
                print(result)
                if result.startswith("RESULT"):
                    encrypted_string = result.split(' ', 1)[1]
                    history.append(('encrypted', encrypted_string))
                log(logger_proc, "ENCRYPT", text)

        elif choice == "3":
            print("1. Enter a new string")
            print("2. Select from history")
            option = input("Choose an option: ")
            if option == "1":
                text = input("Enter a string to decrypt: ")
                result = send_encryption_command(enc_proc, f"DECRYPT {text}")
                print(result)
                log(logger_proc, "DECRYPT", text)
            elif option == "2":
                # Filter history to show only encrypted strings
                encrypted_texts = [item for item in history if item[0] == 'encrypted']
                if not encrypted_texts:
                    print("No encrypted strings available in history.")
                    continue
                for idx, item in enumerate(encrypted_texts):
                    print(f"{idx+1}. {item[1]}")
                selection = int(input("Select a string from history: ")) - 1
                text = encrypted_texts[selection][1]
                result = send_encryption_command(enc_proc, f"DECRYPT {text}")
                print(result)
                log(logger_proc, "DECRYPT", text)

        elif choice == "4":
            print("History:")
            for idx, item in enumerate(history):
                print(f"{idx+1}. {item[1]} ({item[0]})")

        elif choice == "5":
            send_encryption_command(enc_proc, "QUIT")
            log(logger_proc, "QUIT", "Driver program exiting")
            logger_proc.stdin.write("QUIT\n")
            logger_proc.stdin.flush()
            logger_proc.wait()
            enc_proc.wait()
            break

if __name__ == "__main__":
    main()