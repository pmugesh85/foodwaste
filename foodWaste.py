import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3
from twilio.rest import Client

# Twilio credentials
account_sid = 'AC38cbb7f731cc2ffa037c74ec686c7093'# Replace with your actual SID
auth_token = '89fae8b54b7837b05f2319bd7a91437e'      # Replace with your actual Auth Token
client = Client(account_sid, auth_token)

# Twilio phone number (replace with your Twilio number)
twilio_number = '+18642077443'

# Phone number to send notification to (replace with the client's phone number)
client_number = '+917708500797'

# Create the main window
window = tk.Tk()
window.title("Login & Signup Form")
window.geometry('340x440')
window.configure(bg='#333333')

# Variables to store the user credentials
stored_username = ""
stored_password = ""

# Function to handle login
def login():
    global stored_username, stored_password
    # Check if the entered credentials match the stored credentials
    if username_entry.get() == stored_username and password_entry.get() == stored_password:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        window.withdraw()  # Hide the login window
        open_food_management()  # Open the food management window
    else:
        messagebox.showerror(title="Error", message="Invalid login. Please sign up if you haven't.")
6
# Function to handle signup
def signup():
    global stored_username, stored_password
    # Check if the fields are filled and passwords match
    if signup_username_entry.get() and signup_password_entry.get() == signup_confirm_password_entry.get():
        stored_username = signup_username_entry.get()  # Store the username
        stored_password = signup_password_entry.get()  # Store the password
        messagebox.showinfo(title="Signup Success", message="You successfully signed up. Now log in.")
        show_login()  # Switch to the login page
    else:
        messagebox.showerror(title="Error", message="Passwords do not match or missing fields.")

# Function to show the login frame
def show_login():
    signup_frame.pack_forget()
    login_frame.pack()

# Function to show the signup frame
def show_signup():
    login_frame.pack_forget()
    signup_frame.pack()

# --- Login Frame ---
login_frame = tk.Frame(window, bg='#333333')

# Creating login widgets
login_label = tk.Label(
    login_frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tk.Label(
    login_frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(login_frame, font=("Arial", 16))
password_label = tk.Label(
    login_frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_entry = tk.Entry(login_frame, show="*", font=("Arial", 16))
login_button = tk.Button(
    login_frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
switch_to_signup_button = tk.Button(
    login_frame, text="Signup", bg="#333333", fg="#FF3399", font=("Arial", 14), command=show_signup)

# Placing login widgets
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)
switch_to_signup_button.grid(row=4, column=0, columnspan=2)

# --- Signup Frame ---
signup_frame = tk.Frame(window, bg='#333333')

# Creating signup widgets
signup_label = tk.Label(
    signup_frame, text="Signup", bg='#333333', fg="#FF3399", font=("Arial", 30))
signup_username_label = tk.Label(
    signup_frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
signup_username_entry = tk.Entry(signup_frame, font=("Arial", 16))
signup_password_label = tk.Label(
    signup_frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
signup_password_entry = tk.Entry(signup_frame, show="*", font=("Arial", 16))
signup_confirm_password_label = tk.Label(
    signup_frame, text="Confirm Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
signup_confirm_password_entry = tk.Entry(signup_frame, show="*", font=("Arial", 16))
signup_button = tk.Button(
    signup_frame, text="Signup", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=signup)
switch_to_login_button = tk.Button(
    signup_frame, text="Login", bg="#333333", fg="#FF3399", font=("Arial", 14), command=show_login)

# Placing signup widgets
signup_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
signup_username_label.grid(row=1, column=0)
signup_username_entry.grid(row=1, column=1, pady=20)
signup_password_label.grid(row=2, column=0)
signup_password_entry.grid(row=2, column=1, pady=20)
signup_confirm_password_label.grid(row=3, column=0)
signup_confirm_password_entry.grid(row=3, column=1, pady=20)
signup_button.grid(row=4, column=0, columnspan=2, pady=30)
switch_to_login_button.grid(row=5, column=0, columnspan=2)

# --- Food Management Window ---
def open_food_management():
    # Create the food management window
    root = tk.Tk()
    root.title("Food Management")
    root.geometry("800x600")
    root.configure(bg='#333333')

    # Connect to the SQLite database
    conn = sqlite3.connect('food_items.db')
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS FoodItem (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    FoodName TEXT NOT NULL,
                    quantity INTEGER,
                    expiry_date DATE NOT NULL)''')
    conn.commit()

    # Function to reset the AUTOINCREMENT counter
    def reset_autoincrement():
        c.execute("DELETE FROM sqlite_sequence WHERE name='FoodItem'")
        conn.commit()

    # Function to add food item
    def add_food_item():
        food_name = name_entry.get()
        quantity = quantity_entry.get()
        expiry_date = expiry_entry.get()

        if food_name and expiry_date:
            try:
                quantity = int(quantity)  # Convert quantity to integer
                
                c.execute("INSERT INTO FoodItem (FoodName, quantity, expiry_date) VALUES (?, ?, ?)",
                          (food_name, quantity, expiry_date))
                conn.commit()
                messagebox.showinfo("Success", f"Food item '{food_name}' added!")
                name_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                expiry_entry.delete(0, tk.END)

                # Send notification for expiring food items
                check_and_send_expiry_notification()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity (number).")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add food item: {e}")
        else:
            messagebox.showwarning("Input Error", "Please provide food name and expiry date.")

    # Function to display food items in a new window
    def display_food_items_window():
        display_window = tk.Toplevel(root)
        display_window.title("Available FoodItems")
        display_window.geometry("800x600")
        display_window.configure(bg='#333333')
        
        title_label = tk.Label(display_window, text="Available FoodItems", font=("Arial", 16, "bold"), bg='#333333', fg="#FF3399")
        title_label.pack(pady=20)
        
        food_list_display = tk.Listbox(display_window, font=("Courier", 10), width=60, height=15)
        food_list_display.pack(pady=20)

        c.execute("SELECT * FROM FoodItem")
        food_items = c.fetchall()

        for index, item in enumerate(food_items, start=1):
            food_list_display.insert(tk.END, f"{item[0]}. FoodName: {item[1]}, Quantity: {item[2]}, Expiry: {item[3]}")
        
        delete_button_display = tk.Button(display_window, text="Delete Selected Item", command=lambda: delete_selected_food_item_display(food_list_display), font=("Arial", 12), bg="#FF3399", fg="#FFFFFF")
        delete_button_display.pack(pady=10)

    # Function to delete selected food item
    def delete_selected_food_item_display(food_list_display):
        try:
            selected_index = food_list_display.curselection()
            
            if selected_index:
                selected_item = food_list_display.get(selected_index)
                food_id = selected_item.split(".")[0]
                
                c.execute("DELETE FROM FoodItem WHERE id=?", (food_id,))
                conn.commit()

                if c.rowcount > 0:
                    
                    messagebox.showinfo("Success", "Food item deleted!")
                    food_list_display.delete(selected_index)

                    c.execute("SELECT COUNT(*) FROM FoodItem")
                    count = c.fetchone()[0]
                    if count == 0:
                        reset_autoincrement()
                else:
                    messagebox.showwarning("Error", "Failed to delete food item.")
            else:
                messagebox.showwarning("Selection Error", "Please select a food item to delete.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to check for expiring food items and send Twilio notifications
    def check_and_send_expiry_notification():
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        c.execute("SELECT FoodName, expiry_date FROM FoodItem WHERE expiry_date = ?", (tomorrow_date,))
        expiring_items = c.fetchall()

        if expiring_items:
            message = "Food items expiring tomorrow:\n"
            for item in expiring_items:
                message += f"{item[0]} (Expiry: {item[1]})\n"
            
            # Send message via Twilio
            try:
                client.messages.create(
                    body=message,
                    from_=twilio_number,
                    to=client_number
                )
                messagebox.showinfo("Notification", "Expiry notification sent successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send notification: {e}")

    # Custom styles
    label_font = ("Arial", 14, "bold")
    entry_font = ("Arial", 12)
    button_font = ("Arial", 12)
    button_color = "#FF3399"
    button_text_color = "#FFFFFF"

    # Add widgets
    name_label = tk.Label(root, text="Food Name", font=label_font, bg='#333333', fg="#FFFFFF")
    name_entry = tk.Entry(root, font=entry_font, width=30)

    quantity_label = tk.Label(root, text="Quantity", font=label_font, bg='#333333', fg="#FFFFFF")
    quantity_entry = tk.Entry(root, font=entry_font, width=30)

    expiry_label = tk.Label(root, text="Expiry Date (YYYY-MM-DD)", font=label_font, bg='#333333', fg="#FFFFFF")
    expiry_entry = tk.Entry(root, font=entry_font, width=30)

    add_button = tk.Button(root, text="Add FoodItem", command=add_food_item, font=button_font, bg=button_color, fg=button_text_color)
    show_button = tk.Button(root, text="Show FoodItems", command=display_food_items_window, font=button_font, bg=button_color, fg=button_text_color)

    # Place widgets
    name_label.pack(pady=10)
    name_entry.pack(pady=10)
    quantity_label.pack(pady=10)
    quantity_entry.pack(pady=10)
    expiry_label.pack(pady=10)
    expiry_entry.pack(pady=10)
    add_button.pack(pady=20)
    show_button.pack(pady=10)

    # Start the main loop for the food management window
    root.mainloop()

# Start by showing the login frame
login_frame.pack()

# Start the main event loop for the login/signup window
window.mainloop()