import tkinter as tk
from tkinter import messagebox
import pandas as pd
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2
import os
import numpy as np
from tensorflow import keras
import sqlite3

# Load the Keras model
model = keras.models.load_model('C:\\New folder\\Project\\FaultyNonFaulty\\FaultyNonFaulty\\my_model2.h5')



def center_window(window):
    # Calculate the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates for centering the window
    x = (screen_width - window.winfo_reqwidth()) // 3
    y = (screen_height - window.winfo_reqheight()) // 5

    # Set the window's position
    window.geometry("+{}+{}".format(x, y))

def login():
    # Validate login credentials
    login_id = login_id_entry.get()
    password = password_entry.get()
    
    try:
        user_data = pd.read_excel("C:\\New folder\\Project\\FaultyNonFaulty\\FaultyNonFaulty\\users_details.xlsx")
        index = user_data['Username'].eq(login_id).idxmax()
        user_data_login_id = user_data['Username'][index]
        user_data_password = user_data['Password'][index]

        try:
            if login_id == user_data_login_id and password == user_data_password:
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                open_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid login ID or password")
        except Exception as e:
            print(e)
    except FileNotFoundError:
        print(FileNotFoundError)
        messagebox.showerror("Login Failed", "User details file not found")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Please contact your administrator for password reset.")

def open_dashboard():
    # Hide the main window
    window.withdraw()

    def close_dashboard():
        window2.destroy()
        window.deiconify()



    def center_window2(window2):
        # Calculate the screen width and height
        screen_width = window2.winfo_screenwidth()
        screen_height = window2.winfo_screenheight()

        # Calculate the x and y coordinates for centering the window2
        x = (screen_width - window2.winfo_reqwidth()) // 3
        y = (screen_height - window2.winfo_reqheight()) // 5

        # Set the window2's position
        window2.geometry("+{}+{}".format(x, y))

    def open_check_new_batch():
        content_label.pack_forget()
        check_batch_button.pack(pady=10)
        selected_image_label.pack(pady=5)
        upload_button.pack(pady=10)
        image_box.pack(pady=20)
        label_box.pack(pady=5)

    def open_about_us():
        global about
        if not about:
            about =True
            # Hide the existing content
            content_label.pack_forget()
            check_batch_button.pack_forget()
            selected_image_label.pack_forget()
            upload_button.pack_forget()
            label_box.pack_forget()
            image_box.pack_forget()
            about = False

    def about_model():
        global accuracy
        if not accuracy:
            accuracy =True
            # Hide the existing content
            check_batch_button.pack_forget()
            selected_image_label.pack_forget()
            upload_button.pack_forget()
            label_box.pack_forget()
            image_box.pack_forget()
            content_label.pack(pady=100)
            accuracy = False



    # to search file in local directory
    def browse_image():
        # Function to browse and select an image file

        # Open file dialog to select an image file
        filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        print(image_path)
        # print(image_path)
        image_path2 = image_path.split('/')[-1]
        
        if image_path:
            # Update the selected image label with the selected image path
            global selected_image_path
            selected_image_path = image_path

            # print(selected_image_path)
            
            selected_image_label.config(text="Selected Image: " + image_path2)




    def upload_image():
        if selected_image_path:
            image_path = selected_image_path
        else:
            messagebox.showerror("Please Select Image!")

        def preprocess_image(image_path):
            # Load the image using OpenCV
            image = cv2.imread(image_path)
            # Resize the image to match the expected input shape of the model
            resized_image = cv2.resize(image, (150, 150))
            # Normalize the pixel values (if needed)
            normalized_image = resized_image / 255.0  # Assuming the model expects values between 0 and 1
            # Return the preprocessed image
            return normalized_image

        def predict_image_quality(image_path):
            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)
            # Reshape the image to match the input shape of the model
            input_image = np.expand_dims(preprocessed_image, axis=0)
            # Make the prediction
            prediction = (model.predict(input_image) > 0.5).astype("int32")
            # Retrieve the predicted class or quality score (adjust based on your model's output)
            predicted_quality = prediction[0][0]  # Assuming the model predicts a single value
            # Return the predicted quality
            return predicted_quality


        # Dummy function to process the image and generate the label
        def process_image(image_path):
            predicted_quality = predict_image_quality(image_path)
            # Process the image and generate label
            # predicted_quality =1
            if predicted_quality == 0:
                predicted_quality = 'Non Faulty'
            else:
                predicted_quality = 'Faulty'
            label = predicted_quality
            return label


        # Call the function to process the image and generate the label
        label = process_image(image_path)

        # Display the returned image in the image box
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_box.configure(image=photo)
        image_box.image = photo

        # Display the label in the label box
        label_box.configure(text="Label: " + label)
        label_box.image = label



    # Create the main window2
    window2 = tk.Toplevel(window)
    window2.title("Dashboard")
    window2.geometry("600x500")
    center_window2(window2)

    # Create a frame for the content
    content_frame = tk.Frame(window2)
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Set background image
    bg_image = ImageTk.PhotoImage(Image.open("C:\\New folder\\Project\\FaultyNonFaulty\\FaultyNonFaulty\\bg_images\bg2.png"))
    bg_label = tk.Label(content_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a frame for the navigation bar
    nav_frame = tk.Frame(content_frame, bg="skyblue", bd=0)
    nav_frame.pack(side=tk.TOP, fill=tk.X)

    # Create navigation buttons with rounded corners
    button_style = {"bg": "blue", "fg": "white", "font": ("Arial", 12, "bold"), "relief": tk.RAISED, "bd": 4, "borderwidth": 0}
    dashboard_button = tk.Button(nav_frame, text="Dashboard", command=open_check_new_batch, **button_style)
    dashboard_button.pack(side=tk.LEFT, padx=10, pady=5)

    # about_us_button = tk.Button(nav_frame, text="About Us", command=open_about_us, **button_style)
    # about_us_button.pack(side=tk.LEFT, padx=10, pady=5)

    about_model_button = tk.Button(nav_frame, text="About Model", command=about_model, **button_style)
    about_model_button.pack(side=tk.LEFT, padx=10, pady=5)

    # Close button
    close_button = tk.Button(nav_frame, text="Logout",bg='red',fg='white', command=close_dashboard)
    close_button.pack(side=tk.RIGHT, padx=10, pady=5)

    #________________________________Dashboard page content__________________________________#

    # Create label in the dashboard page
    # content_label = tk.Label(content_frame, text="New Job Quality Testing", font=("Arial", 16))
    content_label = tk.Label(content_frame, text="Model Accuracy: 0.89", font=("Arial", 16))
    # content_label.pack(pady=50)

    # Create button in the dashboard page
    check_batch_button = tk.Button(content_frame, text="Check new batch", command=browse_image, bg="green", fg="white", font=("Arial", 12, "bold"))
    check_batch_button.pack(pady=10)

    selected_image_label = tk.Label(content_frame, text="Selected Image: ")
    selected_image_label.pack(pady=5)

    upload_button = tk.Button(content_frame, text="Upload Image", command=upload_image, bg="blue", fg="white", font=("Arial", 12, "bold"))
    upload_button.pack(pady=10)


    image_box = tk.Label(content_frame)
    image_box.pack(pady=20)


    label_box = tk.Label(content_frame, text="Label: ")
    label_box.pack(pady=5)


    # Run the GUI
    window2.mainloop()



def register(username, password, email):
    # Validate registration fields
    if not username or not password or not email:
        messagebox.showerror("Registration Failed", "Please fill in all the fields.")
        return

    # Store user details in Excel file
    data = {"Username": [username], "Password": [password], "Email": [email]}
    df = pd.DataFrame(data)
    
    try:
        existing_data = pd.read_excel("users_details.xlsx")
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_excel("users_details.xlsx", index=False)
        messagebox.showinfo("Registration Successful", "Registration completed successfully!")
    except FileNotFoundError:
        df.to_excel("users_details.xlsx", index=False)
        messagebox.showerror("Registration Failed", "User details file not found")

def open_registration():
    global registration_
    if not registration_:
        registration_ = True

        # Create the registration window
        registration_frame = tk.Frame(window)
        registration_frame.pack()

        # Registration fields
        username_label = tk.Label(registration_frame, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(registration_frame, width=30)
        username_entry.pack(pady=5)

        password_label = tk.Label(registration_frame, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(registration_frame, show="*", width=30)
        password_entry.pack(pady=5)

        email_label = tk.Label(registration_frame, text="Email ID:")
        email_label.pack()
        email_entry = tk.Entry(registration_frame, width=30)
        email_entry.pack(pady=5)

        # Register button
        register_button = tk.Button(registration_frame, text="Register", padx=10, pady=5, bg="green", fg="white", command=lambda: register(username_entry.get(), password_entry.get(), email_entry.get()), width=30)
        register_button.pack(pady=10)

        def close_registration():
            global registration_
            registration_ = False
            # registration_link.config(state=tk.NORMAL)
            registration_frame.destroy()

        # Close button
        close_button = tk.Button(registration_frame, text="Close", padx=10, pady=5, bg="red", fg="white", command=close_registration, width=30)
        close_button.pack()

    else:
        messagebox.showerror("Registration Failed", "Registration page already opened!")

# Create the main window
window = tk.Tk()
window.title("Login Page")
window.geometry("600x500")  # Set size of the main window
center_window(window)


# flags 
registration_ = False
about = False
accuracy = False

# Create login ID label and entry field
login_id_label = tk.Label(window, text="Login ID:")
login_id_label.pack(pady=10)
login_id_entry = tk.Entry(window, width=36)
login_id_entry.pack(pady=10)

# Create password label and entry field
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*", width=36)
password_entry.pack(pady=10)

# Create login button
login_button = tk.Button(window, text="Login", command=login, padx=10, pady=5, bg="green", fg="white", width=30)
login_button.pack(pady=10)

# Create forgot password button
forgot_password_button = tk.Label(window, text="Forgot Password", fg="blue", cursor="hand2", width=30)
forgot_password_button.pack(pady=10)
forgot_password_button.bind("<Button-1>", lambda e: forgot_password())

# Create registration link
registration_link = tk.Label(window, text="Don't have an account? Register here!", fg="blue", cursor="hand2", width=30)
registration_link.pack()
registration_link.bind("<Button-1>", lambda e: open_registration())

# Run the GUI
window.mainloop()
