import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH
from validation_utils import ValidationUtils  # NEW IMPORT


class DriverRegistrationPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Driver Registration")
        self.root.geometry("500x750")  # Made slightly taller
        self.root.configure(bg="#f0f0f5")

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=100)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(
            header_frame,
            text="Driver Registration",
            bg="#DDC01A",
            fg="#ffffff",
            font=("Helvetica", 18, "bold")
        )
        header_label.pack(pady=20)

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="Driver Registration Form", bg="#ffffff", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Name Entry
        tk.Label(main_frame, text="Name:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.name_entry.pack(pady=5)

        # Email Entry
        tk.Label(main_frame, text="Email:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        self.email_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.email_entry.pack(pady=5)

        # Phone Number Entry
        tk.Label(main_frame, text="Phone Number:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        self.phone_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.phone_entry.pack(pady=5)

        # Password Entry
        tk.Label(main_frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Min 6 chars, letters & numbers)", bg="#ffffff", 
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
            width=34, 
            show="*"
        )
        self.password_entry.grid(row=0, column=0, padx=(0, 5))

        self.show_password = tk.BooleanVar(value=False)
        
        def toggle_password():
            self.password_entry.config(show="" if self.show_password.get() else "*")

        toggle_button = tk.Checkbutton(
            password_frame,
            text="Show",
            variable=self.show_password,
            command=toggle_password,
            bg="#ffffff",
            font=("Helvetica", 10)
        )
        toggle_button.grid(row=0, column=1)

        # License Number Entry
        tk.Label(main_frame, text="License Number:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Example: DL1234567890)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        self.license_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.license_entry.pack(pady=5)

        # Vehicle Number Entry
        tk.Label(main_frame, text="Vehicle Number:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Example: KA01AB1234)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        self.vehicle_number_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.vehicle_number_entry.pack(pady=5)

        # Vehicle Type Dropdown
        tk.Label(main_frame, text="Vehicle Type:", bg="#ffffff", font=("Helvetica", 12)).pack(anchor="w", pady=5)
        self.vehicle_type_var = tk.StringVar(value="Select")
        vehicle_type_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.vehicle_type_var,
            values=["Sedan", "SUV", "Hatchback", "Van", "Bike"],
            state="readonly",
            font=("Helvetica", 12),
            width=37
        )
        vehicle_type_combobox.pack(pady=5)

        # Register Button
        register_button = tk.Button(
            main_frame,
            text="Register Driver",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.perform_registration
        )
        register_button.pack(pady=15)

        # Back Button
        back_button = tk.Button(
            main_frame,
            text="Back to Dashboard",
            bg="#000000",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            relief="flat",
            command=self.back_to_dashboard
        )
        back_button.pack(pady=5)

    def perform_registration(self):
        """Handle driver registration with ALL VALIDATIONS"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_var.get().strip()
        license_no = self.license_entry.get().strip()
        vehicle_number = self.vehicle_number_entry.get().strip()
        vehicle_type = self.vehicle_type_var.get()

        # ✅ VALIDATION 1: Check all fields
        if not all([name, email, phone, password, license_no, vehicle_number]) or vehicle_type == "Select":
            messagebox.showerror("Error", "All fields are required!")
            return

        # ✅ VALIDATION 2: Validate name
        is_valid, error_msg = ValidationUtils.validate_name(name, "Driver Name")
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg)
            self.name_entry.focus()
            return

        # ✅ VALIDATION 3: Validate email
        is_valid, error_msg = ValidationUtils.validate_email(email)
        if not is_valid:
            messagebox.showerror("Invalid Email", error_msg)
            self.email_entry.focus()
            return

        # ✅ VALIDATION 4: Validate phone
        is_valid, error_msg = ValidationUtils.validate_phone(phone)
        if not is_valid:
            messagebox.showerror("Invalid Phone Number", error_msg)
            self.phone_entry.focus()
            return

        # ✅ VALIDATION 5: Validate password
        is_valid, error_msg = ValidationUtils.validate_password(password)
        if not is_valid:
            messagebox.showerror("Weak Password", error_msg)
            self.password_entry.focus()
            return

        # ✅ VALIDATION 6: Validate license number
        is_valid, error_msg = ValidationUtils.validate_license_number(license_no)
        if not is_valid:
            messagebox.showerror("Invalid License Number", error_msg)
            self.license_entry.focus()
            return

        # ✅ VALIDATION 7: Validate vehicle number
        is_valid, error_msg = ValidationUtils.validate_vehicle_number(vehicle_number)
        if not is_valid:
            messagebox.showerror("Invalid Vehicle Number", error_msg)
            self.vehicle_number_entry.focus()
            return

        # Clean phone number
        phone_clean = phone.replace("+977", "").replace("977", "").replace("-", "").replace(" ", "")
        if phone_clean.startswith("01"):
            phone_clean = phone_clean[2:]

        # Clean license and vehicle numbers
        license_clean = license_no.strip().upper()
        vehicle_clean = vehicle_number.strip().upper().replace(" ", "").replace("-", "")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # ✅ VALIDATION 8: Check if email already exists
            cursor.execute("SELECT COUNT(*) FROM drivers WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Email Already Exists", "This email is already registered as a driver.")
                self.email_entry.focus()
                return

            # ✅ VALIDATION 9: Check if phone already exists
            cursor.execute("SELECT COUNT(*) FROM drivers WHERE phone = ?", (phone_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Phone Number Exists", "This phone number is already registered.")
                self.phone_entry.focus()
                return

            # ✅ VALIDATION 10: Check if license already exists
            cursor.execute("SELECT COUNT(*) FROM drivers WHERE license_number = ?", (license_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("License Already Registered", "This license number is already registered.")
                self.license_entry.focus()
                return

            # ✅ VALIDATION 11: Check if vehicle already exists
            cursor.execute("SELECT COUNT(*) FROM drivers WHERE vehicle_number = ?", (vehicle_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Vehicle Already Registered", "This vehicle number is already registered.")
                self.vehicle_number_entry.focus()
                return

            # Insert driver
            query = """
                INSERT INTO drivers (name, email, phone, password, license_number, vehicle_number, vehicle_type, status,)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'available')
            """
            cursor.execute(query, (name, email, phone_clean, password, license_clean, vehicle_clean, vehicle_type))
            conn.commit()

            messagebox.showinfo(
                "✅ Registration Successful!", 
                f"Driver {name} has been registered successfully!\n\n"
                f"Email: {email}\n"
                f"License: {license_clean}\n"
                f"Vehicle: {vehicle_clean} ({vehicle_type})\n\n"
                f"Status: Available for bookings"
            )
            self.clear_fields()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database Error", "License number or vehicle number already exists.")
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        """Clear all input fields"""
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.password_var.set("")
        self.license_entry.delete(0, tk.END)
        self.vehicle_number_entry.delete(0, tk.END)
        self.vehicle_type_var.set("Select")

    def back_to_dashboard(self):
        """Close window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DriverRegistrationPage(root)
    root.mainloop()