import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Use PIL for image handling



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
    welcome_label.pack(anchor="w", pady=(60, 20), padx=(80, 0))

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
    input_frame.pack(expand=True, pady=(38, 0), padx=(20, 0), anchor="nw")

    # Button
    def load():
        print("Submit clicked!")  # Replace with actual function

    entryfont = ("Nunito SemiBold", 12)
    email_entry = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    email_entry.grid(row=2, columnspan=2, sticky="nw", pady=(0, 0), padx=(10, 0))

    pass_entry = tk.Entry(input_frame, fg="black", width=24, font=entryfont)
    pass_entry.grid(row=3, columnspan=2, sticky="nw", pady=(20, 0), padx=(10, 0))

    signup = tk.Button(input_frame, text="Sign up", bg="#601E88", fg="white", command=load, width=24, font=entryfont)
    signup.grid(row=4, columnspan=3, sticky="nw", pady=(40, 0), padx=(10, 0))
    # Run the Tkinter event loop
    root.mainloop()
