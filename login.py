import tkinter as tk
from tkinter import messagebox
import sqlite3
from config import DB_PATH, COLORS


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        
        # FULLSCREEN/MAXIMIZED
        self.root.state('zoomed')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#000000")

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=100)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Welcome to Taxi Booking System",
            bg="#DDC01A",
            fg="#000000",
            font=("Helvetica", 22, "bold")
        )
        header_label.pack(pady=30)

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ffffff", pady=20, padx=20, bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="Login", bg="#ffffff", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Email Entry
        tk.Label(main_frame, text="Email:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        self.email_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=30)
        self.email_entry.pack(pady=5)

        # Password Entry
        tk.Label(main_frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        self.password_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=30, show="*")
        self.password_entry.pack(pady=5)

        # Show Password Checkbox
        self.show_password_var = tk.IntVar()
        show_password_check = tk.Checkbutton(
            main_frame,
            text="Show Password",
            variable=self.show_password_var,
            bg="#ffffff",
            font=("Helvetica", 10),
            command=self.toggle_password_visibility
        )
        show_password_check.pack(pady=5)

        # Login Button
        login_button = tk.Button(
            main_frame,
            text="Login",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=25,
            relief="flat",
            command=self.perform_login
        )
        login_button.pack(pady=15)

        # Registration Section
        tk.Label(
            main_frame, 
            text="─────────── New User? ───────────", 
            bg="#ffffff", 
            font=("Helvetica", 10),
            fg="#666666"
        ).pack(pady=(10, 5))

        # Customer Register Button
        customer_register_button = tk.Button(
            main_frame,
            text="👤 Register as Customer",
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=25,
            relief="flat",
            command=self.open_customer_register
        )
        customer_register_button.pack(pady=5)

        # Driver Register Button
        driver_register_button = tk.Button(
            main_frame,
            text="🚗 Register as Driver",
            bg="#28a745",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=25,
            relief="flat",
            command=self.open_driver_register
        )
        driver_register_button.pack(pady=5)

        # Info label
        info_label = tk.Label(
            main_frame,
            text="ℹ️ Driver accounts require admin approval",
            bg="#fff3cd",
            fg="#856404",
            font=("Helvetica", 9),
            pady=5
        )
        info_label.pack(pady=5, fill="x")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    def perform_login(self):
        """Handle login process"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Validation Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Check customer
            cursor.execute("SELECT * FROM customers WHERE email = ? AND password = ?", (email, password))
            customer = cursor.fetchone()
            if customer:
                messagebox.showinfo("Login Success", f"Welcome {customer[1]}!")
                self.open_dashboard('customer', customer[0], customer[3], customer[1])
                return

            # Check driver
            cursor.execute("SELECT * FROM drivers WHERE email = ? AND password = ?", (email, password))
            driver = cursor.fetchone()
            if driver:
                cursor.execute("SELECT status FROM drivers WHERE driver_id = ?", (driver[0],))
                driver_status = cursor.fetchone()[0]
                
                if driver_status == 'pending':
                    messagebox.showwarning(
                        "Account Pending", 
                        f"Welcome {driver[1]}!\n\n"
                        "Your driver account is pending admin approval.\n"
                        "You will be notified once your account is approved.\n\n"
                        "Please contact admin for more information."
                    )
                    return
                elif driver_status == 'rejected':
                    messagebox.showerror(
                        "Account Rejected", 
                        "Your driver account application was not approved.\n"
                        "Please contact admin for more information."
                    )
                    return
                else:
                    messagebox.showinfo("Login Success", f"Welcome {driver[1]}!")
                    self.open_dashboard('driver', driver[0], driver[2], driver[1])
                    return

            # Check admin
            cursor.execute("SELECT * FROM admin WHERE email = ? AND password = ?", (email, password))
            admin = cursor.fetchone()
            if admin:
                messagebox.showinfo("Login Success", f"Welcome {admin[1]} (Admin)!")
                self.open_dashboard('admin', admin[0], admin[2], admin[1])
                return

            messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        finally:
            if conn:
                conn.close()

    def open_dashboard(self, user_type, user_id, email, name):
        """Open appropriate dashboard"""
        self.root.destroy()
        new_root = tk.Tk()
        
        if user_type == 'customer':
            from customer_dashboard import CustomerDashboard
            CustomerDashboard(new_root, email, name, user_id)
        elif user_type == 'driver':
            from driver_dashboard import DriverDashboard
            DriverDashboard(new_root, email, name, user_id)
        elif user_type == 'admin':
            from admin_dashboard import AdminDashboard
            AdminDashboard(new_root, email, name, user_id)

    def open_customer_register(self):
        """Open customer registration page"""
        self.root.destroy()
        new_root = tk.Tk()
        from register import RegisterPage
        RegisterPage(new_root)

    def open_driver_register(self):
        """Open driver registration page"""
        self.root.destroy()
        new_root = tk.Tk()
        from driver_self_register import DriverSelfRegistrationPage
        DriverSelfRegistrationPage(new_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()