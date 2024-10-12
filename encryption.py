#!/usr/bin/env python
import sys

# Define the passkey as a global variable
passkey = None

# Function to perform Vigenère cipher encryption
def vigenere_encrypt(text, key):
    result = []
    key = key.upper()
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i % len(key)]) - ord('A')
            encrypted_char = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
            result.append(encrypted_char)
        else:
            result.append(char)
    return ''.join(result)

# Function to perform Vigenère cipher decryption
def vigenere_decrypt(text, key):
    result = []
    key = key.upper()
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i % len(key)]) - ord('A')
            decrypted_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
            result.append(decrypted_char)
        else:
            result.append(char)
    return ''.join(result)

# Main function that listens for commands
def main():
    global passkey  # Access the global passkey variable
    while True:
        command = sys.stdin.readline().strip()  # Read from stdin
        if command == "QUIT":
            break
        elif command.startswith("PASSKEY "):
            passkey = command.split(" ", 1)[1]  # Set the passkey
            print("RESULT")
            sys.stdout.flush()
        elif command.startswith("ENCRYPT "):
            if passkey is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
                text = command.split(" ", 1)[1]  # Get the text to encrypt
                result = vigenere_encrypt(text, passkey)  # Encrypt the text
                print(f"RESULT {result}")
                sys.stdout.flush()
        elif command.startswith("DECRYPT "):
            if passkey is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
                text = command.split(" ", 1)[1]  # Get the text to decrypt
                result = vigenere_decrypt(text, passkey)  # Decrypt the text
                print(f"RESULT {result}")
                sys.stdout.flush()
        else:
            print("ERROR Unknown command")
            sys.stdout.flush()

if __name__ == "__main__":
    main()