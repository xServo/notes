from tkinter import *
from cryptography.fernet import Fernet 
import os

root = Tk()
root.configure()

# config
notes_file = "notes"
keys_file = "keys" # CHANGE THIS TO A FLASH DRIVE A LOCATION ON A FLASHDRIVE

# clears terminal
def tk_clear():
        for widget in root.winfo_children():
            widget.destroy()

def header(text, span):
    lbl = Label(root, text=text)
    lbl.grid(column=1, row=1, columnspan=span)


def refresh():
    with open(notes_file, "r") as f:
        global notes 
        global tokens
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

def get_note(name_entry, entry_entry):
    name = name_entry.get()
    name = name + "\n"
    entry = entry_entry.get()
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
    start()

# adds note
def add_note():
    tk_clear()
    # gets name
    header("Enter a name for your note. (this will be unencrypted)", 1)
    name_entry = Entry(root)
    name_entry.grid(row=2, column=1)
    # gets note
    lbl = Label(root, text="Enter your note. (this will be encrypted)")
    lbl.grid(column=1, row=3, columnspan=1)
    entry_entry = Entry(root, fg="red")
    entry_entry.grid(row=4, column=1)
    # done button
    btn = Button(text="Done", command=lambda: get_note(name_entry, entry_entry))
    btn.grid(column=1, row=5)

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

# read notes
def read_display(note):
    global selection
    tk_clear()
    title = notes[int(note) - 1] + ":"
    header(title, 1)
    lbl = Label(root, text=decrypt(note))
    lbl.grid(column=1, row=2, columnspan=1)
    btn = Button(root, text="Done", command=start)
    btn.grid(column=1, row=3, columnspan=1)

def read():
        tk_clear()
        lbl = Label(root, text="Select a note to read.")
        lbl.grid(column=1, row=1, columnspan=3)
        button = []
        cnt = 0
        for i in notes:
            cnt +=1
            button.append(Button(root, text=i, command=lambda cnt=cnt: read_display(cnt)))
            button[cnt - 1].grid(column=cnt, row=2)

def start():
    tk_clear()
    # begin
    refresh()
    # main display
    display = "Please select an option."
    lbl = Label(root, text=display)
    lbl.grid(column=1, row=1, columnspan=2)
    # buttons
    read_button = Button(root, text="Read Notes", command=read)
    read_button.grid(column=1, row=2)
    add_button = Button(root, text="Add Notes", command=add_note)
    add_button.grid(column=2, row=2)

start()
root.mainloop()
