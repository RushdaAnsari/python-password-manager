import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from random import randint, shuffle, choice
import pyperclip
import json


class PasswordManager:
    def __init__(self):
        #----------------------------------------UI SETUP--------------------------------------#   
         
        # window setting
        self.root = tk.Tk()
        self.root.geometry("350x343")
        self.root.title("Password Manager")
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(file="img/key.png"))

        # background image
        self.bgimg = tk.PhotoImage(file="img/logo.png")
        self.limg= Label(self.root, i=self.bgimg, justify=tk.CENTER)
        self.limg.grid(row=0, column=1, pady=10)

        # adding widgets
        # website label
        self.web_label = Label(text="Website", pady=5, padx=10)
        self.web_label.grid(row=1)
        # website entry box
        self.web = Entry(width=42)
        self.web.grid(row=1, column=1, columnspan=2)
        # cursor inside website entry box
        self.web.focus()

        # email label
        self.email_label = Label(text="Username", pady=5, padx=10)
        self.email_label.grid(row=2)
        # email entry box
        self.email = Entry(width=42)
        self.email.grid(row=2, column=1, columnspan=2)
        self.email.insert(0, "example@gmail.com")

        # password label
        self.password_label = Label(text="Password", pady=5, padx=10)
        self.password_label.grid(row=3)
        # password entry box
        self.password = Entry(width=42)
        self.password.grid(row=3, column=1, columnspan=2)

        # password generator button
        self.password_generator_btn = Button(text="Generate Password", width=17, bg="dodgerblue", command=self.password_generator)
        self.password_generator_btn.grid(row=4, column=1)
        self.password_generator_btn.place(x=78, y=270)

        # search button
        self.search_btn = Button(text="Search", bg="limegreen", width=16, command=self.search)
        self.search_btn.grid(row=4, column=2)
        self.search_btn.place(x=210, y=270)

        # save button
        self.save_btn = Button(text="Save Password", width=35, bg="gold", command=self.save)
        self.save_btn.grid(row=5, column=1, columnspan=2, pady=37)

        # mainloop
        self.root.mainloop()
    
    #----------------------------------------SAVING FUNCTION--------------------------------------#    
    def save(self):
        # getting hold of website entry
        website = self.web.get()
        # getting hold of email entry
        email = self.email.get()
        # getting hold of password entry
        password = self.password.get()
        # saving it in a dict format
        new_data = {
            website: {
            "email": email,
            "password": password
            }
        }
        # checking if any field is empty
        if len(website) == 0 or len(password) == 0 or len(email) == 0:
            # popup for empty field
            messagebox.showinfo(title="Oops",message="Make sure any field is not left empty!")
        else:
            try:
                # open file and load data
                with open("password.json", "r") as data_file:
                    data = json.load(data_file)   
                # raising exception if file not found
            except FileNotFoundError:
                # create new file
                with open("password.json", "w") as data_file:
                    # add data
                    json.dump(new_data, data_file, indent=4)
            else:
                # if file found then update
                data.update(new_data) 
                # write new data in file
                with open("password.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                # popup after saving password
                messagebox.showinfo(title="Password Manager", message="Password Saved.")
                # delete entries after saving
                self.web.delete(0, END) 
                self.password.delete(0, END)

    #---------------------------------RANDOM PASSWORD GENERATOR--------------------------------------#    
    def password_generator(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        # pick 5-8 random letters
        password_letters = [choice(letters) for _ in range(randint(5, 8))]
        # pick 2-3 random symbols
        password_symbols = [choice(symbols) for _ in range(randint(2, 3))]
        # pick 2-3 random numbers
        password_numbers = [choice(numbers) for _ in range(randint(2, 3))]
        # add all in the list
        password_list = password_letters + password_numbers + password_symbols
        # shuffle
        shuffle(password_list)
        # concatenate it into a single string
        password = "".join(password_list)
        # delete previous password from password entry box
        self.password.delete(0, END)
        # write new password
        self.password.insert(0, password)
        # automatically save password to clipboard
        pyperclip.copy(password)

    #----------------------------------------SEARCH FUNCTION--------------------------------------#    
    def search(self):
        # get website entry
        website = self.web.get()
        # open data file
        with open("password.json") as data_file:
            # load data
            data = json.load(data_file)
        # check if website is in the data
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            # display email and password for that website
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        # if website in not in the data 
        elif website not in data:
            # popup
            messagebox.showinfo(title="Error", message="No data found with this input. Please check spelling and letter casing.")



PasswordManager()