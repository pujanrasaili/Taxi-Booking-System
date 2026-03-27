import tkinter as tk
from tkinter import messagebox
import sqlite3
from config import DB_PATH
from validation_utils import ValidationUtils


class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Register Page")
        
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
            text="Create Your Account",
            bg="#DDC01A",
            fg="#ffffff",
            font=("Helvetica", 25, "bold")
        )
        header_label.pack(pady=30)

        # Main Container
        main_container = tk.Frame(self.root, bg="#000000")
        main_container.pack(fill="both", expand=True)

        from tkinter import ttk
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

        main_frame = tk.Frame(scrollable_frame, bg="#ffffff", pady=20, padx=20, bd=2, relief="groove")
        main_frame.pack(pady=20, padx=20)

        tk.Label(main_frame, text="Register", bg="#ffffff", font=("Helvetica", 22, "bold")).pack(pady=10)

        # Name Entry
        tk.Label(main_frame, text="Name:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35)
        self.name_entry.pack(pady=5)

        # Address Entry
        tk.Label(main_frame, text="Address:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.address_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35)
        self.address_entry.pack(pady=5)

        # Email Entry
        tk.Label(main_frame, text="Email:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.email_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35)
        self.email_entry.pack(pady=5)

        # Phone Number Entry
        tk.Label(main_frame, text="Phone Number:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.phone_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35)
        self.phone_entry.pack(pady=5)

        # Password Entry
        tk.Label(main_frame, text="Password:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(main_frame, text="(Min 6 characters, must have letters & numbers)", bg="#ffffff", 
                font=("Helvetica", 9), fg="#666666").pack(anchor="w", pady=(0,5))
        self.password_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35, show="*")
        self.password_entry.pack(pady=5)

        # Confirm Password Entry
        tk.Label(main_frame, text="Confirm Password:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.confirm_password_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35, show="*")
        self.confirm_password_entry.pack(pady=5)

        # Show Password Checkbox
        self.show_password_var = tk.IntVar()
        show_password_check = tk.Checkbutton(
            main_frame,
            text="Show Passwords",
            variable=self.show_password_var,
            bg="#ffffff",
            font=("Helvetica", 10),
            command=self.toggle_password_visibility
        )
        show_password_check.pack(pady=5)

        # Register Button
        register_button = tk.Button(
            main_frame,
            text="Register",
            bg="#000000",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=25,
            relief="flat",
            command=self.perform_registration
        )
        register_button.pack(pady=20)

        # Back to Login Button
        back_button = tk.Button(
            main_frame,
            text="← Back to Login",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=25,
            relief="flat",
            command=self.navigate_to_login
        )
        back_button.pack(pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
            self.confirm_password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            self.confirm_password_entry.config(show="*")

    def perform_registration(self):
        """Handle registration process with ALL VALIDATIONS"""
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not name or not address or not email or not password or not confirm_password or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        is_valid, error_msg = ValidationUtils.validate_name(name, "Name")
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg)
            self.name_entry.focus()
            return

        is_valid, error_msg = ValidationUtils.validate_address(address)
        if not is_valid:
            messagebox.showerror("Invalid Address", error_msg)
            self.address_entry.focus()
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
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please enter the same password.")
            self.confirm_password_entry.focus()
            return

        phone_clean = phone.replace("+977", "").replace("977", "").replace("-", "").replace(" ", "")
        if phone_clean.startswith("01"):
            phone_clean = phone_clean[2:]

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM customers WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Email Already Exists", "This email is already registered. Please use a different email or login.")
                self.email_entry.focus()
                return

            cursor.execute("SELECT COUNT(*) FROM customers WHERE phone = ?", (phone_clean,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Phone Number Exists", "This phone number is already registered.")
                self.phone_entry.focus()
                return

            query = "INSERT INTO customers (name, address, email, password, phone) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (name, address, email, password, phone_clean))
            conn.commit()

            messagebox.showinfo(
                "✅ Registration Successful!", 
                f"Welcome {name}!\n\nYour account has been created successfully.\n\nYou can now login with your credentials."
            )
            self.navigate_to_login()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists. Please use a different email.")
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn:
                conn.close()

    def navigate_to_login(self):
        """Navigate to login page"""
        self.root.destroy()
        from login import LoginPage
        new_root = tk.Tk()
        LoginPage(new_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterPage(root)
    root.mainloop()