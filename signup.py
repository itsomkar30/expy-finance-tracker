import tkinter as tk
from tkinter import PhotoImage
import requests
from PIL import Image, ImageTk  # Use PIL for image handling
from firebase import auth
from siginin import sign_in_page


def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def sign_up_page():
    # Create the main window
    root = tk.Tk()
    root.geometry("600x480")
    root.resizable(0, 0)
    root.title("Sign-up ExPy")

    # Fonts
    nunito2 = ("Nunito ExtraBold", 22)
    nunitosemi2 = ("Nunito SemiBold", 14)

    # Load images using PIL
    img = Image.open("assets/finance.jpg")
    email_icon_data = Image.open("assets/user.png")
    password_icon_data = Image.open("assets/lock.png")

    # Convert PIL images to ImageTk format for tkinter compatibility
    image = ImageTk.PhotoImage(img.resize((300, 400)))
    user_icon = ImageTk.PhotoImage(email_icon_data.resize((19, 19)))
    password_icon = ImageTk.PhotoImage(password_icon_data.resize((20, 20)))

    # Left side: Image Label
    Lside = tk.Label(root, image=image)
    Lside.pack(expand=True, side="left")

    # Right side: Frame with form elements
    frame = tk.Frame(root, width=300, height=480, bg="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    # Welcome Text Label
    welcome_label = tk.Label(frame, text="Welcome!", fg="#601E88", bg="#ffffff", anchor="w", justify="left",
                             font=nunito2)
    welcome_label.pack(anchor="w", pady=(60, 0), padx=(80, 0))

    # Subtitle Label
    subtitle_label = tk.Label(frame, text="Sign up to your account", fg="#7E7E7E", bg="#ffffff", anchor="w",
                              justify="left", font=nunitosemi2)
    subtitle_label.pack(anchor="w", padx=(40, 0))

    # User icon with label
    # Uncomment if you want to use the user icon image
    # user_label = tk.Label(frame, text="  User: ", fg="#601E88", bg="#ffffff", anchor="w", font=("Arial Bold", 15), image=user_icon, compound="left")
    # user_label.pack(anchor="w", pady=(38, 0), padx=(25, 0))

    # Input section Frame
    input_frame = tk.Frame(frame, bg="#ffffff")
    input_frame.pack_propagate(0)
    input_frame.pack(expand=True, pady=(30, 0), padx=(20, 0), anchor="nw")

    entryfont = ("Nunito SemiBold", 12)
    new_email_entry = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    new_email_entry.grid(row=2, columnspan=2, sticky="nw", pady=(0, 0), padx=(10, 0))
    add_placeholder(new_email_entry, "Enter your email")
    # new_email = new_email_entry.get().strip()

    new_pass_entry = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    new_pass_entry.grid(row=3, columnspan=2, sticky="nw", pady=(20, 0), padx=(10, 0))
    add_placeholder(new_pass_entry, "Enter Password")
    # new_password = new_pass_entry.get().strip()

    new_pass_entry_confirm = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    new_pass_entry_confirm.grid(row=4, columnspan=2, sticky="nw", pady=(20, 0), padx=(10, 0))
    add_placeholder(new_pass_entry_confirm, "Confirm Password")

    # new_password_confirm = new_pass_entry_confirm.get().strip()

    # def signup_database():
    #     if new_password == new_password_confirm:
    #         auth.create_user_with_email_and_password(new_email, new_password)
    #         print("Signed up!")

    def signup_database():
        new_email = new_email_entry.get().strip()
        new_password = new_pass_entry.get().strip()
        new_password_confirm = new_pass_entry_confirm.get().strip()

        if new_password == new_password_confirm:
            try:
                auth.create_user_with_email_and_password(new_email, new_password)
                print("Signed up successfully!")
                signup_result_label.config(text="Signed up successfully!")
            except requests.exceptions.HTTPError as e:
                print("User already exists")
                signup_result_label.config(text="User already exists")
                # print(f"Error: {e}")
        else:
            print("Passwords do not match")
            signup_result_label.config(text="Passwords do not match")

    signup = tk.Button(input_frame, text="Sign up", bg="#601E88", fg="white", command=signup_database, width=24,
                       font=entryfont)
    signup.grid(row=5, columnspan=3, sticky="nw", pady=(25, 0), padx=(10, 0))

    signup_result_label = tk.Label(input_frame, text="", fg="red", bg="#ffffff", anchor="center",
                                   justify="center")
    signup_result_label.grid(row=6, columnspan=3, sticky="n", pady=(30, 0), padx=(10, 0))

    go_to_signin_label = tk.Label(input_frame, text="Try Sign-in instead", fg="red", bg="#ffffff", anchor="center",
                                  justify="center", cursor="hand2", underline=True)
    go_to_signin_label.grid(row=7, columnspan=3, sticky="n", pady=(30, 0), padx=(10, 0))

    go_to_signin_label.bind("<Button-1>", lambda e: access_signin_from_signup())

    def access_signin_from_signup():
        root.destroy()
        sign_in_page()

    root.mainloop()
