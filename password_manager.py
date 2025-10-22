# Password Manager by Khaleel Theophile
# Simple password manager using AES encryption (cryptography)

import json
import os
from cryptography.fernet import Fernet

# Generate encryption key if it doesn't exist
def generate_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        print("Encryption key created! Keep this file safe.")
    else:
        print("Key already exists. Skipping key generation.")

# Load encryption key
def load_key():
    return open("key.key", "rb").read()

# Add a new password
def add_password():
    site = input("Enter site/app name: ")
    username = input("Enter username/email: ")
    password = input("Enter password: ")
    data = {"site": site, "username": username, "password": password}

    # Check if passwords.json exists and is valid JSON
    passwords = []
    if os.path.exists("passwords.json"):
        try:
            with open("passwords.json", "r") as f:
                passwords = json.load(f)
        except json.JSONDecodeError:
            # File exists but empty or invalid
            passwords = []

    passwords.append(data)
    with open("passwords.json", "w") as f:
        json.dump(passwords, f, indent=4)

    print(f"Added password for {site}!")

# Encrypt passwords.json
def encrypt_file():
    if not os.path.exists("passwords.json"):
        print("No passwords to encrypt yet. Add some first!")
        return

    key = load_key()
    fernet = Fernet(key)
    with open("passwords.json", "rb") as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open("passwords.json", "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    print("Passwords encrypted successfully!")

# Decrypt passwords.json
def decrypt_file():
    if not os.path.exists("passwords.json"):
        print("No passwords file found to decrypt.")
        return

    key = load_key()
    fernet = Fernet(key)
    with open("passwords.json", "rb") as enc_file:
        encrypted = enc_file.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        with open("passwords.json", "wb") as dec_file:
            dec_file.write(decrypted)
        print("Passwords decrypted successfully!")
    except Exception as e:
        print("Decryption failed. Maybe the file is not encrypted or corrupted.")

# Main menu
def main():
    generate_key()
    while True:
        print("\n===== PASSWORD MANAGER =====")
        print("1. Add new password")
        print("2. Encrypt passwords")
        print("3. Decrypt passwords")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_password()
        elif choice == "2":
            encrypt_file()
        elif choice == "3":
            decrypt_file()
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice. Try again!")

# Run the program
if __name__ == "__main__":
    main()
