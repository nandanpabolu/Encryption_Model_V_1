import subprocess
import sys
import os

def run_logger(log_file):
    return subprocess.Popen(['python3', 'logger.py', log_file], stdin=subprocess.PIPE, text=True)

def run_encryption():
    return subprocess.Popen(['python3', 'encryption.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

def log(logger_proc, action, message):
    logger_proc.stdin.write(f"{action} {message}\n")
    logger_proc.stdin.flush()

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

    history = []
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
            print("1. Enter a new password")
            print("2. Select from history")
            option = input("Choose an option: ")
            if option == "1":
                password = input("Enter a new password: ")
                send_encryption_command(enc_proc, f"PASSKEY {password}")
                log(logger_proc, "PASSKEY", "Password set")
            elif option == "2":
                if history:
                    for idx, item in enumerate(history):
                        print(f"{idx+1}. {item}")
                    selection = int(input("Select a string from history: ")) - 1
                    password = history[selection]
                    send_encryption_command(enc_proc, f"PASSKEY {password}")
                    log(logger_proc, "PASSKEY", "Password set from history")
                else:
                    print("No history available")

        elif choice == "2":
            print("1. Enter a new string")
            print("2. Select from history")
            option = input("Choose an option: ")
            if option == "1":
                text = input("Enter a string to encrypt: ")
                result = send_encryption_command(enc_proc, f"ENCRYPT {text}")
                print(result)
                if result.startswith("RESULT"):
                    history.append(text)
                log(logger_proc, "ENCRYPT", text)
            elif option == "2":
                if history:
                    for idx, item in enumerate(history):
                        print(f"{idx+1}. {item}")
                    selection = int(input("Select a string from history: ")) - 1
                    text = history[selection]
                    result = send_encryption_command(enc_proc, f"ENCRYPT {text}")
                    print(result)
                    log(logger_proc, "ENCRYPT", text)
                else:
                    print("No history available")

        elif choice == "3":
            print("1. Enter a new string")
            print("2. Select from history")
            option = input("Choose an option: ")
            if option == "1":
                text = input("Enter a string to decrypt: ")
                result = send_encryption_command(enc_proc, f"DECRYPT {text}")
                print(result)
                if result.startswith("RESULT"):
                    history.append(text)
                log(logger_proc, "DECRYPT", text)
            elif option == "2":
                if history:
                    for idx, item in enumerate(history):
                        print(f"{idx+1}. {item}")
                    selection = int(input("Select a string from history: ")) - 1
                    text = history[selection]
                    result = send_encryption_command(enc_proc, f"DECRYPT {text}")
                    print(result)
                    log(logger_proc, "DECRYPT", text)
                else:
                    print("No history available")

        elif choice == "4":
            print("History:")
            for idx, item in enumerate(history):
                print(f"{idx+1}. {item}")

        elif choice == "5":
            send_encryption_command(enc_proc, "QUIT")
            log(logger_proc, "QUIT", "Driver program exiting")
            logger_proc.stdin.write("QUIT\n")
            logger_proc.stdin.flush()
            break

if __name__ == "__main__":
    main()