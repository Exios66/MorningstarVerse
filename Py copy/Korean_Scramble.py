import random
import datetime


# Cipher mapping according to the provided key
cipher_mapping = {
    'A': '가', 'B': '나', 'C': '다', 'D': '라', 'E': '마', 'F': '바', 'G': '사', 'H': '아', 'I': '자', 'J': '차', 'K': '카', 'L': '타',
    'M': '파', 'N': '하', 'O': '거', 'P': '너', 'Q': '더', 'R': '러', 'S': '머', 'T': '버', 'U': '서', 'V': '어', 'W': '저', 'X': '처',
    'Y': '커', 'Z': '터',
    'a': '각', 'b': '낙', 'c': '닥', 'd': '락', 'e': '막', 'f': '박', 'g': '삭', 'h': '악', 'i': '작', 'j': '착', 'k': '칵', 'l': '탁',
    'm': '팍', 'n': '학', 'o': '걱', 'p': '넉', 'q': '덕', 'r': '럭', 's': '먹', 't': '벅', 'u': '석', 'v': '엉', 'w': '정', 'x': '청',
    'y': '켕', 'z': '텅'
}

# Reverse the mapping for decryption
reverse_cipher_mapping = {v: k for k, v in cipher_mapping.items()}

# Function to encrypt a term using the cipher mapping
def encrypt_term(term):
    encrypted_term = ''.join([cipher_mapping.get(char, char) for char in term])
    return encrypted_term

# Function to add null characters and irrelevant sequences for obfuscation
def add_obfuscation(encrypted_term):
    # Define some null characters and irrelevant sequences
    null_characters = ['허', '경', '고', '로', '미']
    irrelevant_sequences = ['사랑', '하늘', '바다', '별', '꽃']

    # Insert null characters at random positions
    obfuscated_term = list(encrypted_term)
    for _ in range(random.randint(1, 3)):  # Add 1 to 3 null characters
        position = random.randint(0, len(obfuscated_term))
        obfuscated_term.insert(position, random.choice(null_characters))

    # Insert irrelevant sequences at random positions
    for _ in range(random.randint(1, 2)):  # Add 1 to 2 irrelevant sequences
        position = random.randint(0, len(obfuscated_term))
        obfuscated_term.insert(position, random.choice(irrelevant_sequences))

    return ''.join(obfuscated_term)

# Function to lock the term with a four-digit alphanumeric code
def lock_with_pin(term):
    pin_code = input("Enter a four-digit alphanumeric pin code: ")
    while len(pin_code) != 4 or not pin_code.isalnum():
        print("Invalid pin code. Please enter a four-digit alphanumeric pin code.")
        pin_code = input("Enter a four-digit alphanumeric pin code: ")
    return f"{term}{pin_code}"

# Function to decrypt a term
def decrypt_term(encrypted_term):
    # Remove null characters and irrelevant sequences
    cleaned_term = encrypted_term
    null_characters = ['허', '경', '고', '로', '미']
    irrelevant_sequences = ['사랑', '하늘', '바다', '별', '꽃']

    for null_char in null_characters:
        cleaned_term = cleaned_term.replace(null_char, '')

    for irrelevant_sequence in irrelevant_sequences:
        cleaned_term = cleaned_term.replace(irrelevant_sequence, '')

    # Decrypt the cleaned term using the reverse cipher mapping
    decrypted_term = ''
    i = 0
    while i < len(cleaned_term):
        for symbol in reverse_cipher_mapping.keys():
            if cleaned_term.startswith(symbol, i):
                decrypted_term += reverse_cipher_mapping[symbol]
                i += len(symbol)
                break
        else:
            decrypted_term += cleaned_term[i]  # If no match found, keep the original character
            i += 1

    return decrypted_term

# Save the encrypted term to a local file
def save_to_file(obfuscated_term, association):
    # Open the file with UTF-8 encoding to support Unicode characters
    with open("encrypted_scrambles.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"## Scramble Entry - {timestamp}\n")
        file.write(f"- **Association**: {association}\n")
        file.write(f"- **Obfuscated Scramble**: {obfuscated_term}\n")
        file.write("\n\n")
    print("**Scramble saved to `encrypted_scrambles.txt`.**")

# Load and reveal scrambles from the file
def load_and_reveal_scrambles():
    try:
        # Open the file with UTF-8 encoding to handle Unicode characters
        with open("encrypted_scrambles.txt", "r", encoding="utf-8") as file:
            scrambles = file.read().strip().split("## Scramble Entry")
            scrambles = [entry for entry in scrambles if entry.strip()]

            if not scrambles:
                print("**No scrambles found.**")
                return

            # Sort the scrambles by the timestamp
            scrambles.sort(key=lambda x: x.split(' - ')[1].strip())

            # Display the list of scrambles
            print("\n## Saved Scrambles")
            print("=" * 40)
            for i, entry in enumerate(scrambles):
                try:
                    timestamp = entry.split(' - ')[1].strip().split('\n')[0]
                    association = entry.split('**Association**: ')[1].split('\n')[0].strip()
                    print(f"**{i + 1}.** **Saved on:** {timestamp} | **Association:** {association}")
                except IndexError:
                    print(f"**{i + 1}.** Invalid entry format, skipping...")

            # Get the user's choice
            print("\n")
            choice = int(input("**Select the number of the scramble to reveal:** "))
            if 1 <= choice <= len(scrambles):
                selected_entry = scrambles[choice - 1]
                try:
                    obfuscated_scramble = selected_entry.split('**Obfuscated Scramble**: ')[1].split('\n')[0]
                    decrypted_term = decrypt_term(obfuscated_scramble)
                    print(f"**Decrypted Term:** {decrypted_term}")
                except IndexError:
                    print("**Selected entry is corrupted or improperly formatted.**")
                else:
                    print("**Invalid selection.**")
                print("**Invalid selection.**")
    except FileNotFoundError:
        print("**No scrambles found.**")

# Clear the contents of the storage file
def clear_storage_file():
    confirm = input("**Are you sure you want to clear all saved scrambles? This cannot be undone. (y/n):** ").lower()
    if confirm == 'y':
        with open("encrypted_scrambles.txt", "w", encoding="utf-8") as file:
            file.write("")  # Clear the file content
        print("**All scrambles have been cleared.**")
    else:
        print("**Operation cancelled.**")

STORAGE_FILE = "encrypted_scrambles.txt"  # Add this line to define the storage file

def main():
    print("# Korean Symbol Cipher Tool")
    print("Choose an action:")
    print("- (e) Encrypt a new term")
    print("- (r) Reveal an existing term")
    print("- (v) View all scrambles")
    print("- (c) Clear the storage file")

    action = input("\n**Your choice (e/r/v/c):** ").lower()

    if action == 'e':
        term = input("**Enter the word, phrase, or scramble to encrypt:** ")
        association = input("**Association?:** ").strip()
        if not association:
            association = "No Association"

        encrypted_term = encrypt_term(term)
        obfuscated_term = add_obfuscation(encrypted_term)
        
        # Lock the term with a pin code
        locked_term = lock_with_pin(obfuscated_term)

        # Confirm details before saving
        print("\n## Term Details")
        print("- **Original Term:**", term)
        print("- **Obfuscated Term:**", obfuscated_term)
        print("- **Locked Term:**", locked_term)
        print("- **Association:**", association)
        confirm = input("\n**Do you want to save this scramble? (y/n):** ").lower()
        if confirm == 'y':
            save_to_file(obfuscated_term, association)
        else:
            print("**Scramble not saved.**")
    elif action == 'r':
        load_and_reveal_scrambles()
    elif action == 'v':
        load_and_reveal_scrambles()  # This could be modified to only view without revealing
    elif action == 'c':
        clear_storage_file()
    else:
        print("**Invalid option.**")

if __name__ == "__main__":
    main()

# End of Selection
    input("\nPress Enter to return to the main menu...")

    print("\n# Korean Symbol Cipher Tool")
    print("Choose an action:")
    print("- (e) Encrypt a new term")
    print("- (r) Reveal an existing term")
    print("- (v) View all scrambles")
    print("- (c) Clear the storage file")
    print("- (x) Exit")

    action = input("\n**Your choice (e/r/v/c/x):** ").lower()

    if action == 'e':
        term = input("**Enter the word, phrase, or scramble to encrypt:** ")
        association = input("**Association?:** ").strip()
        if not association:
            association = "No Association"

        encrypted_term = encrypt_term(term)
        obfuscated_term = add_obfuscation(encrypted_term)

        # Confirm details before saving
        print("\n## Term Details")
        print("- **Original Term:**", term)
        print("- **Obfuscated Term:**", obfuscated_term)
        print("- **Association:**", association)
        confirm = input("\n**Do you want to save this scramble? (y/n):** ").lower()
        if confirm == 'y':
            save_to_file(obfuscated_term, association)
        else:
            print("**Scramble not saved.**")
    elif action == 'r':
        load_and_reveal_scrambles()
    elif action == 'v':
        try:
            with open(STORAGE_FILE, "r") as file:
                scrambles = file.read().strip().split("## Scramble Entry")
                scrambles = [entry for entry in scrambles if entry.strip()]
        except FileNotFoundError:
            print("No scrambles found.")
        else:
            # Sort the scrambles by the timestamp
            scrambles.sort(key=lambda x: x.split(' - ')[1].strip())

            # Display the list of scrambles
            print("\nSaved Scrambles:")
            for i, entry in enumerate(scrambles):
                timestamp = entry.split(' - ')[1].strip().split('\n')[0]
                association = entry.split('**Association**: ')[1].split('\n')[0].strip()
                print(f"{i + 1}. Saved on {timestamp} - Association: {association}")

            # Get the user's choice
            choice = int(input("\nSelect the number of the scramble to view: "))
            if 1 <= choice <= len(scrambles):
                selected_entry = scrambles[choice - 1]
                encoded_scramble = selected_entry.split('`')[1]
                print(f"Encoded Scramble: {encoded_scramble}")
            else:
                print("Invalid selection.")
    elif action == 'c':
        clear_storage_file()
    elif action == 'x':
        print("**Be Great Today.**")
        exit()
    else:
        print("**Invalid option.**")

