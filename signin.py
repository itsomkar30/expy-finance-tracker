import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Use PIL for image handling
from firebase import auth
# from check import main_gui
# from check import check_user_status
from tracker import main


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


def sign_in_page():
    # Create the main window
    root = tk.Tk()
    root.geometry("600x480")
    root.resizable(0, 0)
    root.title("Sign-in ExPy")

    # Fonts
    nunito1 = ("Nunito ExtraBold", 22)
    nunitosemi1 = ("Nunito SemiBold", 14)

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
    welcome_label = tk.Label(frame, text="Welcome back!", fg="#601E88", bg="#ffffff", anchor="w", justify="left",
                             font=nunito1)
    welcome_label.pack(anchor="w", pady=(60, 20), padx=(50, 0))

    # Subtitle Label
    subtitle_label = tk.Label(frame, text="Sign in to your account", fg="#7E7E7E", bg="#ffffff", anchor="w",
                              justify="left", font=nunitosemi1)
    subtitle_label.pack(anchor="w", padx=(55, 0))

    # User icon with label
    # Uncomment if you want to use the user icon image
    # user_label = tk.Label(frame, text="  User: ", fg="#601E88", bg="#ffffff", anchor="w", font=("Arial Bold", 15), image=user_icon, compound="left")
    # user_label.pack(anchor="w", pady=(38, 0), padx=(25, 0))

    # Input section Frame
    input_frame = tk.Frame(frame, bg="#ffffff")
    input_frame.pack_propagate(0)
    input_frame.pack(expand=True, pady=(38, 0), padx=(20, 0), anchor="nw")

    entryfont = ("Nunito SemiBold", 12)
    email_entry = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    email_entry.grid(row=2, columnspan=2, sticky="nw", pady=(0, 0), padx=(10, 0))
    add_placeholder(email_entry, "Enter your email")
    # email = email_entry.get()

    pass_entry = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    pass_entry.grid(row=3, columnspan=2, sticky="nw", pady=(20, 0), padx=(10, 0))
    add_placeholder(pass_entry, "Enter Password")

    # password = pass_entry.get()

    def signin_database():
        email = email_entry.get()
        password = pass_entry.get()

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_uid = user['localId']
            print(f"Signed in! User [ {user_uid} ]")
            signin_result_label.config(text="Signed in successfully!")
            # check_user_status(user_uid)
            root.destroy()
            main(user)


        except:
            print("Invalid email password")
            signin_result_label.config(text="Invalid email password combination")

    signin = tk.Button(input_frame, text="Sign in", bg="#601E88", fg="white", command=signin_database, width=24,
                       font=entryfont)
    signin.grid(row=4, columnspan=3, sticky="nw", pady=(40, 0), padx=(10, 0))

    signin_result_label = tk.Label(input_frame, text="", fg="red", bg="#ffffff", anchor="center",
                                   justify="center")
    signin_result_label.grid(row=5, columnspan=3, sticky="n", pady=(30, 0), padx=(10, 0))

    # Run the Tkinter event loop
    root.mainloop()
