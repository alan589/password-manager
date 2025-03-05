import random
from tkinter import *
from tkinter import messagebox
from random import randint
import pyperclip as pc
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [random.choice(letters) for _ in range(randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def copy_password():
    pc.copy(password_entry.get())
    messagebox.showinfo(title="Password", message="Copied! :)")


def find_password():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Data", message="No data file found.")

    else:
        website = website_entry.get()
        if website in data:
            login = data[website]["login"]
            password =  data[website]["password"]
            messagebox.showinfo(title=f"{website}", message=f"    Login: {login}\n    Password: {password}")
        else:
            messagebox.showinfo(title="Data", message="No details for the website exists.")

def save_password():
    website = website_entry.get()
    login = login_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "login": login,
            "password": password
        }
    }
    if website == "" or login == "" or password == "":
        messagebox.showerror(title="Invalid field", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                data.update(new_data)
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            login_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()





# ---------------------------- UI SETUP ------------------------------- #

FONT = ("Arial", 9, "bold")

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)


# Labels
website_label = Label(text="Website:", padx=35, font=FONT)
website_label.grid(column=0, row=1)

login_label = Label(text="Login:", font=FONT)
login_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=FONT)
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=30, borderwidth=2)
website_entry.grid(column=1, row=1, sticky="W", ipady=2)
website_entry.focus()

login_entry = Entry(width=30, borderwidth=2)
login_entry.grid(column=1, row=2, columnspan=2, sticky="EW", ipady=2, pady=3)

password_entry = Entry(width=30, borderwidth=2)
password_entry.grid(column=1, row=3, sticky="W", ipady=2)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password, width=20, font=FONT)
generate_button.grid(column=2, row=3, sticky="W")

add_button = Button(text="Add", command=save_password, width=17, font=FONT)
add_button.grid(column=0, row=4, pady=20, columnspan=2)

copy_button = Button(text="Copy password", width=17, font=FONT, command=copy_password)
copy_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=find_password, width=20, font=FONT)
search_button.grid(column=2, row=1, sticky="W")



window.mainloop()