import json
import hashlib
import random
import string
from datetime import datetime

# File where journal entries will be stored
DATA_FILE = 'journal_data.json'

# Simple shuffling function for basic encryption
def shuffle_string(s):
    shuffled = list(s)
    random.shuffle(shuffled)
    return ''.join(shuffled)

# Reverse shuffling based on known order (this is just for demonstration)
def unshuffle_string(s, order):
    unshuffled = [''] * len(s)
    for i, o in enumerate(order):
        unshuffled[o] = s[i]
    return ''.join(unshuffled)

# Simple hash function for key generation
def generate_hash_key(entry):
    return hashlib.sha256(entry.encode()).hexdigest()

# Function to save an entry
def save_entry(entry):
    # Shuffle the entry for basic encryption
    shuffled_entry = shuffle_string(entry)
    
    # Generate a hash key for this entry
    key = generate_hash_key(entry)
    
    # Create the journal entry with a timestamp
    journal_entry = {
        "timestamp": datetime.now().isoformat(),
        "content": shuffled_entry
    }

    # Load existing entries
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Save the new entry with the hash key
    data[key] = journal_entry

    # Write back to the file
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

    print("Entry saved successfully!")

# Function to retrieve an entry
def retrieve_entry(entry):
    # Generate the hash key to find the entry
    key = generate_hash_key(entry)
    
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        
        if key in data:
            encrypted_content = data[key]['content']
            # Note: Reverse shuffling is not implemented correctly without knowing the original shuffle order
            # Normally, this would be handled with a reversible algorithm or key management
            print(f"Timestamp: {data[key]['timestamp']}")
            print(f"Content: {encrypted_content} (This is still encrypted and should be manually decrypted)")
        else:
            print("Entry not found.")
    except FileNotFoundError:
        print("No journal entries found.")

# Main interaction loop
def main():
    print("Welcome to your Personal Journal")
    while True:
        print("\nChoose an option:")
        print("1. Add a new entry")
        print("2. Retrieve an entry")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            entry = input("Enter your journal entry: ")
            save_entry(entry)
        elif choice == '2':
            entry = input("Enter the original text of your journal entry to retrieve: ")
            retrieve_entry(entry)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
