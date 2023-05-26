from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    if len(password_entry.get()) == 0:
        password_entry.insert(INSERT, password)
        pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_entry.get().title()
    username = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Empty field(s)", message="You need to fill all the info to save the password.")

    else:
        try:
            with open("data.json", "r") as file:
                # Read old data
                data = json.load(file)

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open("data.json", "w") as file:
                # If no file or no data in file, create or populate file)
                json.dump(new_data, file, indent=4)

        else:
            # Update with new data
            data.update(new_data)

            with open("data.json", "w") as file:
                # Write updated data
                json.dump(data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()

# ---------------------------- LOOKUP PASSWORD ------------------------------- #


def lookup_password():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="No passwords", message="There are no passwords yet. Please add some before searching.")
    else:
        website = website_entry.get().title()
        if len(website) != 0:
            if website in data:
                username = data[website]['email']
                password = data[website]['password']
                messagebox.showinfo(title=f"{website}",
                                message=f"email: {username}\npassword: {password}")
            else:
                messagebox.showinfo(title=f"No passwords for {website}",
                                message=f"There are no passwords for {website} yet")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# LABELS

website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", bg="white")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3)

# ENTRIES

website_entry = Entry(width=24)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_entry = Entry(width=47)
email_entry.insert(INSERT, "*******")
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=24)
password_entry.grid(column=1, row=3)

# BUTTONS

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

generate_password_button = Button(text="Generate Password", command=generate_password, width=18)
generate_password_button.grid(column=2, row=3)

lookup_password_button = Button(text="Search", command=lookup_password, width=18)
lookup_password_button.grid(column=2, row=1)


window.mainloop()
