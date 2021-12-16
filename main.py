import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '@', '^', '=', '%', '&', '(', ')', '*', '+', '[', ']']


def generate_password():
    password_list = []
    password_list += [random.choice(letters) for _ in range(0, random.randint(3, 6))]
    password_list += [random.choice(numbers) for _ in range(0, random.randint(3, 6))]
    password_list += [random.choice(symbols) for _ in range(0, random.randint(3, 6))]

    random.shuffle(password_list)
    password = "".join(password_list)

    entry_password.delete(0, END)
    entry_password.insert(0, password)
    pyperclip.copy(password)


def save_data(new_data):
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open("data.json", mode="w") as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)
        with open("data.json", mode="w") as file:
            json.dump(data, file, indent=4)
    finally:
        entry_website.delete(0, END)
        entry_email_username.delete(0, END)
        entry_password.delete(0, END)


def save():
    website = entry_website.get()
    email = entry_email_username.get()
    password = entry_password.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or email == '' or password == '':
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        save_data(new_data)


def find_password():
    website_key = entry_website.get()
    if len(website_key) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave website empty!")
    else:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
            if website_key in data:
                email = data[website_key]['email']
                password = data[website_key]['password']
                messagebox.showinfo(title=website_key, message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Not found website", message=f"Not found password to {website_key}")
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No data file found")


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)
window.resizable(0, 0)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(130, 100, image=logo_image)

# Components
label_website = Label(text="Website:")
label_email_username = Label(text="Email/Username:")
label_password = Label(text="Password:")
entry_website = Entry(width=21)
entry_email_username = Entry(width=35)
entry_password = Entry(width=21)
btn_generate = Button(text="Generate Password", command=generate_password)
btn_add = Button(text="Add", width=36, command=save)
search_button = Button(text="Search", command=find_password)

# Grid layout
canvas.grid(row=0, column=1)

label_website.grid(row=1, column=0)
entry_website.grid(row=1, column=1)
search_button.grid(row=1, column=2, columnspan=2, sticky="EW")
entry_website.focus()

label_email_username.grid(row=2, column=0)
entry_email_username.grid(row=2, column=1, columnspan=2, sticky="EW")

label_password.grid(row=3, column=0)
entry_password.grid(row=3, column=1)
btn_generate.grid(row=3, column=2)

btn_add.grid(row=4, column=1, columnspan=2)

window.mainloop()
