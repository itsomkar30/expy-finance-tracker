import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Use PIL for image handling
from signin import sign_in_page
from signup import sign_up_page
import os
import json
from firebase import auth
from tracker import main



DATA_FILE = 'logged_user.json'
def load_id():
    """Load expenses from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []



id = load_id()
# print(id)
if id:
    user = auth.sign_in_with_email_and_password(id['user'], id['password'])
    main(user)
    pass
else:
    # Create the main window
    root = tk.Tk()
    root.geometry("600x480")
    root.resizable(0, 0)
    root.title("ExPy - Finance Tracker")

    # Fonts
    nunito = ("Nunito ExtraBold", 25)
    nunitosemi = ("Nunito SemiBold", 12)

    # Load images using PIL
    img = Image.open("assets/finance.jpg")

    # Convert PIL images to ImageTk format for tkinter compatibility
    image = ImageTk.PhotoImage(img.resize((300, 480)))

    # Left side: Image Label
    frame = tk.Frame(root, width=300, height=480, bg="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="left")
    Lside = tk.Label(frame, image=image)
    Lside.pack(expand=True, side="left")

    # Right side: Frame with form elements
    frame = tk.Frame(root, width=300, height=480, bg="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    # Welcome Text Label
    welcome_label = tk.Label(frame, text="Expy", fg="#601E88", bg="#ffffff", anchor="w", justify="left", font=nunito)
    welcome_label.pack(anchor="w", pady=(60, 0), padx=(110, 0))

    # Subtitle Label
    subtitle_label = tk.Label(frame, text="Start Tracking Your Expenses Now!", fg="#7E7E7E", bg="#ffffff", anchor="w",
                              justify="left", font=nunitosemi)
    subtitle_label.pack(anchor="w", pady=(20, 0), padx=(15, 0))

    # Input section Frame
    input_frame = tk.Frame(frame, bg="#ffffff")
    input_frame.pack_propagate(0)
    input_frame.pack(expand=True, pady=(38, 0), padx=(20, 0), anchor="nw")




    def sign_in_method():
        root.destroy()
        sign_in_page()


    def sign_up_method():
        root.destroy()
        sign_up_page()


    signin = tk.Button(input_frame, text="Log in", bg="#601E88", fg="white", command=sign_in_method, width=30)
    signin.grid(row=2, columnspan=3, sticky="nw", pady=(30, 0), padx=(25, 0))

    signup = tk.Button(input_frame, text="Sign up", bg="#601E88", fg="white", command=sign_up_method, width=30)
    signup.grid(row=3, columnspan=3, sticky="nw", pady=(30, 0), padx=(25, 0))

    # Run the Tkinter event loop
    root.mainloop()
