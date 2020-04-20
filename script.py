from cryptography.fernet import Fernet 
import os

# config
notes_file = "notes"
keys_file = "keys" # CHANGE THIS TO A FLASH DRIVE A LOCATION ON A FLASHDRIVE

# clears terminal
def clear():
    os.system("clear")
 #   print("CLEARED") # for testing

# displays name of notes 
def search():
    print("Notes:")
    for i in range(0, len(notes)):
        print("(" + str(i + 1) + ")", notes[i])
        
# adds note
def add_note():
    name = input("Enter the name for your note. (this will be unencrypted)\n")
    name = name + "\n"
    entry = input("Enter your note. (this will be encrypted)\n")
    # encrypt entry
    entry = entry.encode(encoding="UTF-8")
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(entry)
    key_str = key.decode(encoding="UTF-8")
    token_str = token.decode(encoding="UTF-8")
    # add key to keys file
    with open(keys_file, "a") as f:
        key_str = key_str + "\n"
        f.write(key_str)
    # add name and token to notes file
    token_str = token_str + "\n"
    with open(notes_file, "a") as f:
        f.write(name)
        f.write(token_str)

# decrypt token
def decrypt(selection):
    # get key
    with open(keys_file, "r") as f:
        line = f.readline()
        key_lines = []
        cnt = 0
        while line:
            key_lines.append(line.strip())
            cnt += 1
            line = f.readline()
        f = Fernet(key_lines[int(selection) - 1])
        token = tokens[int(selection) - 1]
        token_b = token.encode(encoding="UTF-8")
        decrypted = f.decrypt(token_b)
        decrypted = decrypted.decode(encoding="UTF-8")
        return decrypted


clear()
print("Welcome to Encrypted Notes")
while True:
    # appends each line in notes file to table
    with open(notes_file, "r") as f:
        notes = []
        tokens = []
        line = f.readline()
        cnt = 0
        while line:
            if cnt % 2 == 0:
                notes.append(line.strip())
            if cnt % 2 != 0:
                tokens.append(line.strip())
            cnt += 1
            line = f.readline()

    # Select action
    action = input("What would you like to do?\n(1) Read Notes\n(2) Take Notes\n(3) Exit\n")

    # Read Notes
    if action == "1":
        clear()
        search()
        selection = input("Select a note\n")
        clear()
        print(notes[int(selection) - 1] + ":")
        print(decrypt(selection))
#        print(tokens[int(selection) - 1])
        input("Press ENTER to continue.")
        clear()

    # Take notes
    if action == "2":
        clear()
        add_note()
        clear()

    if action == "3":
        clear()
        break
