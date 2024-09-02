import os
import base64
from datetime import datetime

# Ensure the storage file exists
STORAGE_FILE = "user_supplied_scrambles.txt"
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        f.write("")

# XOR-based encryption
def xor_encrypt_decrypt(data, key):
    key = key * (len(data) // len(key)) + key[:len(data) % len(key)]
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key))

# Encode the scramble using a user-supplied key
def encode_scramble(scramble, key):
    encrypted_data = xor_encrypt_decrypt(scramble, key)
    encoded_scramble = base64.b64encode(encrypted_data.encode()).decode()
    return encoded_scramble

# Decode the scramble using a user-supplied key
def decode_scramble(encoded_scramble, key):
    encrypted_data = base64.b64decode(encoded_scramble).decode()
    decrypted_scramble = xor_encrypt_decrypt(encrypted_data, key)
    return decrypted_scramble

# Save the scramble to a storage file with metadata and two empty lines between entries
def save_scramble_to_file(encoded_scramble, key, association):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    masked_key = f"{key}#####"

    with open(STORAGE_FILE, "a") as file:
        file.write(f"## Scramble Entry - {timestamp}\n")
        file.write(f"- **Association**: {association}\n")
        file.write(f"- **Encoded Scramble**: `{encoded_scramble}`\n")
        file.write(f"- **Key**: `{masked_key}`\n")
        file.write("\n\n")  # Add two empty lines between entries
    print("Scramble saved to user_supplied_scrambles.txt.")

# Load scrambles from the storage file, list them, and allow decoding with the key
def load_and_reveal_scrambles():
    try:
        with open(STORAGE_FILE, "r") as file:
            scrambles = file.read().strip().split("## Scramble Entry")
            scrambles = [entry for entry in scrambles if entry.strip()]

            if not scrambles:
                print("No scrambles found.")
                return

            # Sort the scrambles by the timestamp
            scrambles.sort(key=lambda x: x.split(' - ')[1].strip())

            # Display the list of scrambles
            print("\nSaved Scrambles:")
            for i, entry in enumerate(scrambles):
                timestamp = entry.split(' - ')[1].strip().split('\n')[0]
                association = entry.split('**Association**: ')[1].split('\n')[0].strip()
                print(f"{i + 1}. Saved on {timestamp} - Association: {association}")

            # Get the user's choice
            choice = int(input("\nSelect the number of the scramble to reveal: "))
            if 1 <= choice <= len(scrambles):
                selected_entry = scrambles[choice - 1]
                encoded_scramble = selected_entry.split('`')[1]
                key = input("Enter the key used for encryption: ")
                try:
                    scramble = decode_scramble(encoded_scramble, key)
                    print(f"Decrypted Scramble: {scramble}")
                except:
                    print("Incorrect key or corrupted data.")
            else:
                print("Invalid selection.")
    except FileNotFoundError:
        print("No scrambles found.")

# Clear all saved scrambles
def clear_scrambles():
    confirm = input("Are you sure you want to clear all saved scrambles? This cannot be undone. (y/n): ").lower()
    if confirm == 'y':
        with open(STORAGE_FILE, "w") as file:
            file.write("")  # Clear the file content
        print("All scrambles have been cleared.")
    else:
        print("Operation cancelled.")

# Backup the storage file
def backup_scrambles():
    backup_file = STORAGE_FILE.replace(".txt", "_backup.txt")
    with open(STORAGE_FILE, "r") as file:
        data = file.read()
    with open(backup_file, "w") as file:
        file.write(data)
    print(f"Backup created at {backup_file}")

def main():
    print("User-Supplied Scramble Encryption")
    action = input("Do you want to (e)ncrypt a new scramble, (r)eveal an existing one, (v)iew all scrambles, (c)lear all scrambles, or (b)ackup scrambles? (e/r/v/c/b): ").lower()

    if action == 'e':
        scramble = input("Enter the word, phrase, or scramble to encrypt: ")
        key = input("Enter a key for encryption: ")
        association = input("Association?: ").strip()
        if not association:
            association = "No Association"

        encoded_scramble = encode_scramble(scramble, key)

        # Confirm details before saving
        print("\nScramble Details:")
        print(f"Scramble: {scramble}")
        print(f"Key: {key}")
        print(f"Association: {association}")
        confirm = input("Do you want to save this scramble? (y/n): ").lower()
        if confirm == 'y':
            save_scramble_to_file(encoded_scramble, key, association)
        else:
            print("Scramble not saved.")
    elif action == 'r':
        load_and_reveal_scrambles()
    elif action == 'v':
        load_and_reveal_scrambles()  
    elif action == 'c':
        clear_scrambles()
    elif action == 'b':
        backup_scrambles()
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
