"""
Driver Self-Registration Page
Allows drivers to register themselves with 'pending' status
Admin must approve before they can login
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH
from validation_utils import ValidationUtils


class DriverSelfRegistrationPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Driver Registration")
        
        # ✅ FULLSCREEN FOR POPUP WINDOWS
        self.root.state('zoomed')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#000000")

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=120)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="🚗 Driver Registration",
            bg="#DDC01A",
            fg="#ffffff",
            font=("Helvetica", 24, "bold")
        ).pack(pady=15)
        
        tk.Label(
            header_frame,
            text="Register to become a driver on our platform",
            bg="#DDC01A",
            fg="#ffffff",
            font=("Helvetica", 12)
        ).pack(pady=(0, 15))

        # Main Container with Scrolling
        main_container = tk.Frame(self.root, bg="#000000")
        main_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_container, bg="#000000", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#000000")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        
        def center_window(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', center_window)
        canvas.configure(yscrollcommand=scrollbar.set)

        main_frame = tk.Frame(scrollable_frame, bg="#ffffff", pady=25, padx=25, bd=2, relief="groove")
        main_frame.pack(pady=20, padx=20)

        # Notice Box
        notice_frame = tk.Frame(main_frame, bg="#fff3cd", bd=2, relief="solid", padx=10, pady=10)
        notice_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            notice_frame,
            text="ℹ️ Important Information",
            bg="#fff3cd",
            fg="#856404",
            font=("Helvetica", 12, "bold")
        ).pack(anchor="w")
        
        tk.Label(
            notice_frame,
            text="• Your account will be in 'pending' status after registration\n"
                 "• Admin will review and approve your application\n"
                 "• You will be able to login once approved\n"
                 "• Make sure all information is accurate",
            bg="#fff3cd",
            fg="#856404",
            font=("Helvetica", 10),
            justify="left"
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(main_frame, text="Personal Information", bg="#ffffff", 
                font=("Helvetica", 16, "bold"), fg="#DDC01A").pack(pady=10)

        # Name Entry
        tk.Label(main_frame, text="Full Name:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.name_entry.pack(pady=5)

        # Email Entry
        tk.Label(main_frame, text="Email Address:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.email_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.email_entry.pack(pady=5)

        # Phone Number Entry
        tk.Label(main_frame, text="Phone Number:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(10 digits, starting with 98)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        self.phone_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.phone_entry.pack(pady=5)

        # Password Entry
        tk.Label(main_frame, text="Password:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Min 6 characters, must contain letters & numbers)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        
        password_frame = tk.Frame(main_frame, bg="#ffffff")
        password_frame.pack(pady=5, anchor="w")

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_frame, 
            textvariable=self.password_var, 
            font=("Helvetica", 12), 
            bd=2, 
            relief="solid", 
            width=33, 
            show="*"
        )
        self.password_entry.grid(row=0, column=0, padx=(0, 5))

        self.show_password = tk.BooleanVar(value=False)
        
        def toggle_password():
            self.password_entry.config(show="" if self.show_password.get() else "*")
            self.confirm_password_entry.config(show="" if self.show_password.get() else "*")

        toggle_button = tk.Checkbutton(
            password_frame,
            text="Show",
            variable=self.show_password,
            command=toggle_password,
            bg="#ffffff",
            font=("Helvetica", 10)
        )
        toggle_button.grid(row=0, column=1)

        # Confirm Password
        tk.Label(main_frame, text="Confirm Password:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.confirm_password_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40, show="*")
        self.confirm_password_entry.pack(pady=5)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)
        
        tk.Label(main_frame, text="License & Vehicle Information", bg="#ffffff", 
                font=("Helvetica", 16, "bold"), fg="#DDC01A").pack(pady=10)

        # License Number Entry
        tk.Label(main_frame, text="Driver's License Number:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Example: DL1234567890)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        self.license_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.license_entry.pack(pady=5)

        # Vehicle Number Entry
        tk.Label(main_frame, text="Vehicle Registration Number:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Example: KA01AB1234)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        self.vehicle_number_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.vehicle_number_entry.pack(pady=5)

        # Vehicle Type Dropdown
        tk.Label(main_frame, text="Vehicle Type:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.vehicle_type_var = tk.StringVar(value="Select Vehicle Type")
        vehicle_type_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.vehicle_type_var,
            values=["Sedan", "SUV", "Hatchback", "Van", "Bike"],
            state="readonly",
            font=("Helvetica", 12),
            width=37
        )
        vehicle_type_combobox.pack(pady=5)

        # Terms and Conditions
        self.terms_var = tk.IntVar()
        terms_check = tk.Checkbutton(
            main_frame,
            text="I agree to the terms and conditions",
            variable=self.terms_var,
            bg="#ffffff",
            font=("Helvetica", 11)
        )
        terms_check.pack(pady=15)

        # Register Button
        register_button = tk.Button(
            main_frame,
            text="📝 Submit Registration",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=30,
            relief="flat",
            command=self.perform_registration,
            pady=10
        )
        register_button.pack(pady=15)

        # Back to Login Button
        back_button = tk.Button(
            main_frame,
            text="← Back to Login",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=30,
            relief="flat",
            command=self.navigate_to_login
        )
        back_button.pack(pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def perform_registration(self):
        """Handle driver self-registration with ALL VALIDATIONS"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        license_no = self.license_entry.get().strip()
        vehicle_number = self.vehicle_number_entry.get().strip()
        vehicle_type = self.vehicle_type_var.get()

        if not all([name, email, phone, password, confirm_password, license_no, vehicle_number]):
            messagebox.showerror("Incomplete Form", "All fields are required!")
            return

        if vehicle_type == "Select Vehicle Type":
            messagebox.showerror("Vehicle Type Required", "Please select your vehicle type!")
            return

        if not self.terms_var.get():
            messagebox.showwarning("Terms Required", "Please accept the terms and conditions to continue.")
            return

        is_valid, error_msg = ValidationUtils.validate_name(name, "Full Name")
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg)
            self.name_entry.focus()
            return

        is_valid, error_msg = ValidationUtils.validate_email(email)
        if not is_valid:
            messagebox.showerror("Invalid Email", error_msg)
            self.email_entry.focus()
            return

        is_valid, error_msg = ValidationUtils.validate_phone(phone)
        if not is_valid:
            messagebox.showerror("Invalid Phone Number", error_msg)
            self.phone_entry.focus()
            return

        is_valid, error_msg = ValidationUtils.validate_password(password)
        if not is_valid:
            messagebox.showerror("Weak Password", error_msg)
            self.password_entry.focus()
            return

        if password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match! Please enter the same password.")
            self.confirm_password_entry.focus()
            return

        is_valid, error_msg = ValidationUtils.validate_license_number(license_no)
        if not is_valid:
            messagebox.showerror("Invalid License Number", error_msg)
            self.license_entry.focus()
            return

        is_valid, error_msg = ValidationUtils.validate_vehicle_number(vehicle_number)
        if not is_valid:
            messagebox.showerror("Invalid Vehicle Number", error_msg)
            self.vehicle_number_entry.focus()
            return

        phone_clean = phone.replace("+977", "").replace("977", "").replace("-", "").replace(" ", "")
        if phone_clean.startswith("01"):
            phone_clean = phone_clean[2:]

        license_clean = license_no.strip().upper()
        vehicle_clean = vehicle_number.strip().upper().replace(" ", "").replace("-", "")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM drivers WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Email Already Exists", "This email is already registered. Please use a different email or login.")
                self.email_entry.focus()
                return

            cursor.execute("SELECT COUNT(*) FROM drivers WHERE phone = ?", (phone_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Phone Number Exists", "This phone number is already registered.")
                self.phone_entry.focus()
                return

            cursor.execute("SELECT COUNT(*) FROM drivers WHERE license_number = ?", (license_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("License Already Registered", "This license number is already registered in our system.")
                self.license_entry.focus()
                return

            cursor.execute("SELECT COUNT(*) FROM drivers WHERE vehicle_number = ?", (vehicle_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Vehicle Already Registered", "This vehicle number is already registered in our system.")
                self.vehicle_number_entry.focus()
                return

            query = """
                INSERT INTO drivers (name, email, phone, password, license_number, vehicle_number, vehicle_type, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            """
            cursor.execute(query, (name, email, phone_clean, password, license_clean, vehicle_clean, vehicle_type))
            conn.commit()

            messagebox.showinfo(
                "✅ Registration Submitted Successfully!", 
                f"Thank you for registering, {name}!\n\n"
                f"Your driver account has been created with 'PENDING' status.\n\n"
                f"📋 Next Steps:\n"
                f"1. Admin will review your application\n"
                f"2. You will be notified once approved\n"
                f"3. After approval, you can login with your credentials\n\n"
                f"📧 Email: {email}\n"
                f"🚗 Vehicle: {vehicle_clean} ({vehicle_type})\n\n"
                f"Please contact admin if you have any questions."
            )
            
            self.navigate_to_login()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database Error", "License number or vehicle number already exists.")
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        finally:
            if conn:
                conn.close()

    def navigate_to_login(self):
        """Navigate back to login page"""
        self.root.destroy()
        from login import LoginPage
        new_root = tk.Tk()
        LoginPage(new_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = DriverSelfRegistrationPage(root)
    root.mainloop()