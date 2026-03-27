import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from config import DB_PATH
from register_driver import DriverRegistrationPage
from manage_bookings import ManageBookingsPage


class AdminDashboard:
    def __init__(self, root, admin_email, admin_name, admin_id):
        """Initialize the Admin Dashboard"""
        self.root = root
        self.root.title("Admin Dashboard")
        
        # FULLSCREEN/MAXIMIZED
        self.root.state('zoomed')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#000000")

        self.admin_email = admin_email
        self.admin_name = admin_name
        self.admin_id = admin_id

        # Header Section
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=80)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame,
            text="🎯 Admin Dashboard",
            font=("Helvetica", 20, "bold"),
            bg="#DDC01A",
            fg="white",
        ).pack(pady=20)

        # Create main container with two columns
        main_container = tk.Frame(self.root, bg="#000000")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Column - Admin Info and Statistics
        left_frame = tk.Frame(main_container, bg="#ffffff", bd=2, relief="groove")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Admin Info Section
        admin_info_frame = tk.Frame(left_frame, bg="#f8f9fa", pady=15, padx=15)
        admin_info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(admin_info_frame, text="👤 Admin Information", 
                font=("Helvetica", 14, "bold"), bg="#f8f9fa").pack(pady=(0, 10))
        
        tk.Label(admin_info_frame, text=f"Name: {self.admin_name}", 
                font=("Helvetica", 12), bg="#f8f9fa").pack(pady=3, anchor="w")
        tk.Label(admin_info_frame, text=f"ID: {self.admin_id}", 
                font=("Helvetica", 12), bg="#f8f9fa").pack(pady=3, anchor="w")
        tk.Label(admin_info_frame, text=f"Email: {self.admin_email}", 
                font=("Helvetica", 12), bg="#f8f9fa").pack(pady=3, anchor="w")

        # Statistics Section
        stats_frame = tk.Frame(left_frame, bg="#ffffff", pady=10, padx=15)
        stats_frame.pack(fill="both", padx=10, pady=10)

        tk.Label(stats_frame, text="📊 System Statistics", 
                font=("Helvetica", 14, "bold"), bg="#ffffff").pack(pady=(0, 15))

        # Create statistics cards
        self.create_stat_card(stats_frame, "👥 Total Customers", "total_customers", "#007bff")
        self.create_stat_card(stats_frame, "🚗 Total Drivers", "total_drivers", "#28a745")
        self.create_stat_card(stats_frame, "📋 Total Bookings", "total_bookings", "#ffc107")
        self.create_stat_card(stats_frame, "💰 Total Revenue", "total_revenue", "#dc3545")
        
        # Driver Status Section
        driver_status_outer = tk.Frame(left_frame, bg="#ffffff", pady=15, padx=15, bd=2, relief="solid")
        driver_status_outer.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(driver_status_outer, text="🚦 Driver Status", 
                font=("Helvetica", 13, "bold"), bg="#ffffff").pack(pady=(0, 10))
        
        self.driver_status_list = tk.Frame(driver_status_outer, bg="#ffffff")
        self.driver_status_list.pack(fill="both", expand=True, padx=10)

        # Right Column - Action Buttons
        right_frame = tk.Frame(main_container, bg="#ffffff", bd=2, relief="groove")
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(right_frame, text="⚙️ Management Actions", 
                font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=20)

        # Action Buttons
        button_frame = tk.Frame(right_frame, bg="#ffffff", pady=10)
        button_frame.pack(fill="both", expand=True, padx=20)

        # Driver Registration Button
        register_btn = tk.Button(
            button_frame,
            text="➕ Register New Driver",
            font=("Helvetica", 13, "bold"),
            bg="#007bff",
            fg="white",
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2",
            command=self.register_driver
        )
        register_btn.pack(fill="x", pady=10)

        # Approve Driver Applications Button
        approve_drivers_btn = tk.Button(
            button_frame,
            text="✅ Approve Driver Applications",
            font=("Helvetica", 13, "bold"),
            bg="#ffc107",
            fg="white",
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2",
            command=self.approve_drivers
        )
        approve_drivers_btn.pack(fill="x", pady=10)

        # Assign Drivers Button
        assign_btn = tk.Button(
            button_frame,
            text="🎯 Assign Drivers to Bookings",
            font=("Helvetica", 13, "bold"),
            bg="#28a745",
            fg="white",
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2",
            command=self.manage_bookings
        )
        assign_btn.pack(fill="x", pady=10)

        # View All Bookings Button
        view_bookings_btn = tk.Button(
            button_frame,
            text="📋 View All Bookings",
            font=("Helvetica", 13, "bold"),
            bg="#17a2b8",
            fg="white",
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2",
            command=self.view_all_bookings
        )
        view_bookings_btn.pack(fill="x", pady=10)

        # View All Drivers Button
        view_drivers_btn = tk.Button(
            button_frame,
            text="🚗 View All Drivers",
            font=("Helvetica", 13, "bold"),
            bg="#6f42c1",
            fg="white",
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2",
            command=self.view_all_drivers
        )
        view_drivers_btn.pack(fill="x", pady=10)

        # View All Customers Button
        view_customers_btn = tk.Button(
            button_frame,
            text="👥 View All Customers",
            font=("Helvetica", 13, "bold"),
            bg="#fd7e14",
            fg="white",
            padx=20,
            pady=15,
            relief="flat",
            cursor="hand2",
            command=self.view_all_customers
        )
        view_customers_btn.pack(fill="x", pady=10)

        # Refresh Statistics Button
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Statistics",
            font=("Helvetica", 12),
            bg="#6c757d",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self.load_statistics
        )
        refresh_btn.pack(fill="x", pady=10)

        # Logout Button
        logout_btn = tk.Button(
            button_frame,
            text="🚪 Logout",
            font=("Helvetica", 12),
            bg="#dc3545",
            fg="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self.logout
        )
        logout_btn.pack(fill="x", pady=10)

        # Load initial statistics
        self.load_statistics()

    def create_stat_card(self, parent, title, stat_type, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, bd=2, relief="raised")
        card.pack(fill="x", pady=8)

        tk.Label(card, text=title, font=("Helvetica", 11, "bold"), 
                bg=color, fg="white").pack(pady=(10, 5))
        
        value_label = tk.Label(card, text="Loading...", font=("Helvetica", 18, "bold"), 
                              bg=color, fg="white")
        value_label.pack(pady=(0, 10))
        
        setattr(self, f"{stat_type}_label", value_label)

    def load_statistics(self):
        """Load and display system statistics"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM customers")
            total_customers = cursor.fetchone()[0]
            self.total_customers_label.config(text=str(total_customers))

            cursor.execute("SELECT COUNT(*) FROM drivers")
            total_drivers = cursor.fetchone()[0]
            self.total_drivers_label.config(text=str(total_drivers))

            cursor.execute("SELECT COUNT(*) FROM bookings")
            total_bookings = cursor.fetchone()[0]
            self.total_bookings_label.config(text=str(total_bookings))

            cursor.execute("SELECT SUM(fare) FROM bookings WHERE status = 'completed'")
            total_revenue = cursor.fetchone()[0] or 0
            self.total_revenue_label.config(text=f"₹{total_revenue:.2f}")

            # Driver Status Display
            for widget in self.driver_status_list.winfo_children():
                widget.destroy()

            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM drivers 
                GROUP BY status
            """)
            status_data = cursor.fetchall()
            
            status_dict = {status: count for status, count in status_data}
            
            statuses = [
                ('available', '🟢 Available', '#28a745'),
                ('busy', '🔴 Busy', '#dc3545'),
                ('offline', '⚫ Offline', '#6c757d')
            ]
            
            for status_key, label, color in statuses:
                count = status_dict.get(status_key, 0)
                
                row = tk.Frame(self.driver_status_list, bg="#f8f9fa", 
                              bd=1, relief="solid", pady=8, padx=10)
                row.pack(fill="x", pady=3)
                
                tk.Label(row, text=f"{label}: {count} driver(s)", 
                        font=("Helvetica", 11, "bold"), 
                        bg="#f8f9fa", fg=color, 
                        anchor="w").pack(fill="x")
            
            if total_drivers == 0:
                no_driver_msg = tk.Label(
                    self.driver_status_list,
                    text="⚠️ No drivers registered\nClick 'Register New Driver' to add drivers",
                    font=("Helvetica", 10),
                    bg="#fff3cd",
                    fg="#856404",
                    pady=15,
                    justify="center"
                )
                no_driver_msg.pack(fill="both", expand=True, pady=10)

        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error loading statistics: {err}")
        finally:
            if conn:
                conn.close()

    def register_driver(self):
        """Open Driver Registration window"""
        reg_window = tk.Toplevel(self.root)
        DriverRegistrationPage(reg_window)
        def on_close():
            reg_window.destroy()
            self.load_statistics()
        reg_window.protocol("WM_DELETE_WINDOW", on_close)

    def approve_drivers(self):
        """Open Driver Approval window"""
        approve_window = tk.Toplevel(self.root)
        from approve_drivers import ApproveDriversPage
        ApproveDriversPage(approve_window)
        
        def on_close():
            approve_window.destroy()
            self.load_statistics()
        
        approve_window.protocol("WM_DELETE_WINDOW", on_close)

    def manage_bookings(self):
        """Open Booking Management window"""
        manage_window = tk.Toplevel(self.root)
        ManageBookingsPage(manage_window)

    def view_all_bookings(self):
        """View all bookings in the system"""
        view_window = tk.Toplevel(self.root)
        view_window.title("All Bookings")
        view_window.state('zoomed')
        view_window.configure(bg="#f5f5f5")

        header = tk.Frame(view_window, bg="#DDC01A", height=60)
        header.pack(fill="x")
        tk.Label(header, text="📋 All System Bookings", font=("Helvetica", 18, "bold"),
                bg="#DDC01A", fg="white").pack(pady=15)

        tree_frame = tk.Frame(view_window, bg="#ffffff", padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Customer", "Driver", "Pickup", "Dropoff", "Date", "Time", 
                  "Vehicle", "Distance", "Fare", "Status", "Payment")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            query = """
                SELECT b.booking_id, c.name, COALESCE(d.name, 'Not Assigned'), 
                       b.pickup_location, b.dropoff_location, b.booking_date,
                       substr(b.pickup_time, 12, 5), b.vehicle_type, b.distance, 
                       b.fare, b.status, b.payment_type
                FROM bookings b
                JOIN customers c ON b.customer_id = c.customer_id
                LEFT JOIN drivers d ON b.driver_id = d.driver_id
                ORDER BY b.booking_id DESC
            """
            cursor.execute(query)
            
            for row in cursor.fetchall():
                formatted_row = list(row)
                formatted_row[8] = f"{row[8]:.1f} km" if row[8] else "N/A"
                formatted_row[9] = f"₹{row[9]:.2f}" if row[9] else "₹0.00"
                tree.insert("", "end", values=tuple(formatted_row))
                
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error loading bookings: {err}")
        finally:
            if conn:
                conn.close()

        tk.Button(view_window, text="Close", bg="#dc3545", fg="white", 
                 font=("Helvetica", 12), command=view_window.destroy).pack(pady=10)

    def view_all_drivers(self):
        """View all drivers in the system"""
        view_window = tk.Toplevel(self.root)
        view_window.title("All Drivers")
        view_window.state('zoomed')
        view_window.configure(bg="#f5f5f5")

        header = tk.Frame(view_window, bg="#6f42c1", height=60)
        header.pack(fill="x")
        tk.Label(header, text="🚗 All System Drivers", font=("Helvetica", 18, "bold"),
                bg="#6f42c1", fg="white").pack(pady=15)

        tree_frame = tk.Frame(view_window, bg="#ffffff", padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Email", "Phone", "License", "Vehicle Number", 
                  "Vehicle Type", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT driver_id, name, email, phone, license_number, 
                       vehicle_number, vehicle_type, status
                FROM drivers 
                ORDER BY driver_id
            """)
            
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    display_row = (
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7].upper()
                    )
                    tree.insert("", "end", values=display_row)
            else:
                messagebox.showinfo("No Drivers", "No drivers registered in the system yet.")
                
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error loading drivers: {err}")
        finally:
            if conn:
                conn.close()

        tk.Button(view_window, text="Close", bg="#dc3545", fg="white", 
                 font=("Helvetica", 12), command=view_window.destroy).pack(pady=10)

    def view_all_customers(self):
        """View all customers in the system"""
        view_window = tk.Toplevel(self.root)
        view_window.title("All Customers")
        view_window.state('zoomed')
        view_window.configure(bg="#f5f5f5")

        header = tk.Frame(view_window, bg="#fd7e14", height=60)
        header.pack(fill="x")
        tk.Label(header, text="👥 All System Customers", font=("Helvetica", 18, "bold"),
                bg="#fd7e14", fg="white").pack(pady=15)

        tree_frame = tk.Frame(view_window, bg="#ffffff", padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Email", "Phone", "Registered Date")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT customer_id, name, email, phone, created_at FROM customers ORDER BY customer_id")
            
            for row in cursor.fetchall():
                display_row = list(row)
                if row[4]:
                    display_row[4] = row[4][:10]
                tree.insert("", "end", values=tuple(display_row))
                
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error loading customers: {err}")
        finally:
            if conn:
                conn.close()

        tk.Button(view_window, text="Close", bg="#dc3545", fg="white", 
                 font=("Helvetica", 12), command=view_window.destroy).pack(pady=10)

    def logout(self):
        """Handle logout"""
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            from login import LoginPage
            new_root = tk.Tk()
            LoginPage(new_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root, "admin@example.com", "Admin Name", 1)
    root.mainloop()