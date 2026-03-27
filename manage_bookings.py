import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH


class ManageBookingsPage:
    def __init__(self, root):
        """Initialize the Assign Drivers window"""
        self.root = root
        self.root.title("Assign Drivers to Bookings")
        # NEW LINES (replace with these 4):
        self.root.state('zoomed')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#f5f5f5")
        def __init__(self, root):
        # Header Label
            header_frame = tk.Frame(self.root, bg="#DDC01A")
            header_frame.pack(fill=tk.X)
        
            tk.Label(
            header_frame, 
            text="Assign Drivers to Bookings", 
            font=("Arial", 24, "bold"), 
            bg="#DDC01A", 
            fg="white",
            pady=15
        ).pack()

        # Instructions Label
        instruction_frame = tk.Frame(self.root, bg="#fff3cd", pady=10)
        instruction_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            instruction_frame,
            text="📋 STEP 1: Click on a booking below ➜ STEP 2: Select driver ➜ STEP 3: Click ASSIGN button",
            font=("Arial", 12, "bold"),
            bg="#fff3cd",
            fg="#856404"
        ).pack()

        # Bookings Table
        tk.Label(
            self.root,
            text="Pending Bookings:",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            anchor="w"
        ).pack(fill=tk.X, padx=20, pady=(10, 5))

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        columns = ("Booking ID", "Customer", "Pickup", "Dropoff", "Date", "Time", "Vehicle", "Fare")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        self.tree.heading("Booking ID", text="ID")
        self.tree.heading("Customer", text="Customer")
        self.tree.heading("Pickup", text="Pickup")
        self.tree.heading("Dropoff", text="Dropoff")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Vehicle", text="Vehicle")
        self.tree.heading("Fare", text="Fare")
        
        self.tree.column("Booking ID", width=60)
        self.tree.column("Customer", width=100)
        self.tree.column("Pickup", width=150)
        self.tree.column("Dropoff", width=150)
        self.tree.column("Date", width=100)
        self.tree.column("Time", width=80)
        self.tree.column("Vehicle", width=100)
        self.tree.column("Fare", width=80)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.tree.bind('<<TreeviewSelect>>', self.on_booking_select)

        # Info Label
        self.info_label = tk.Label(
            self.root,
            text="👆 Click on a booking above to see available drivers",
            font=("Arial", 11, "bold"),
            bg="#d4edda",
            fg="#155724",
            pady=10
        )
        self.info_label.pack(fill=tk.X, padx=20, pady=5)

        # DRIVER SELECTION SECTION
        selection_frame = tk.Frame(self.root, bg="#e7f3ff", bd=3, relief="ridge")
        selection_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            selection_frame,
            text="Driver Selection & Assignment",
            font=("Arial", 16, "bold"),
            bg="#e7f3ff",
            fg="#004085"
        ).pack(pady=10)

        # Driver dropdown section
        driver_frame = tk.Frame(selection_frame, bg="#e7f3ff")
        driver_frame.pack(pady=10)

        tk.Label(
            driver_frame, 
            text="Select Driver:", 
            font=("Arial", 14, "bold"), 
            bg="#e7f3ff"
        ).pack(side=tk.LEFT, padx=10)

        self.driver_combobox = ttk.Combobox(
            driver_frame, 
            font=("Arial", 13), 
            width=50, 
            state="readonly"
        )
        self.driver_combobox.pack(side=tk.LEFT, padx=10)

        # BIG ASSIGN BUTTON
        assign_button = tk.Button(
            selection_frame, 
            text="✓ ASSIGN DRIVER TO BOOKING", 
            font=("Arial", 16, "bold"), 
            bg="#28a745", 
            fg="white",
            padx=40,
            pady=15,
            relief="raised",
            bd=4,
            command=self.assign_driver,
            cursor="hand2",
            activebackground="#218838"
        )
        assign_button.pack(pady=15)

        # Bottom buttons
        bottom_frame = tk.Frame(self.root, bg="#f5f5f5")
        bottom_frame.pack(fill=tk.X, pady=10)

        refresh_button = tk.Button(
            bottom_frame,
            text="🔄 Refresh List",
            font=("Arial", 12),
            bg="#6c757d",
            fg="white",
            padx=20,
            pady=8,
            command=self.load_bookings
        )
        refresh_button.pack(side=tk.LEFT, padx=20)

        back_button = tk.Button(
            bottom_frame, 
            text="← Back to Dashboard", 
            font=("Arial", 12), 
            bg="#dc3545", 
            fg="white",
            padx=20,
            pady=8,
            command=self.back_to_dashboard
        )
        back_button.pack(side=tk.RIGHT, padx=20)

        # Load bookings
        self.load_bookings()

    def load_bookings(self):
        """Load pending bookings into the Treeview"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            query = """
                SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location, 
                       b.booking_date, substr(b.pickup_time, 12, 5) as time, 
                       b.vehicle_type, b.fare
                FROM bookings b
                JOIN customers c ON b.customer_id = c.customer_id
                WHERE b.status = 'pending'
                ORDER BY b.booking_date, b.pickup_time
            """
            cursor.execute(query)
            bookings = cursor.fetchall()
            
            # Clear existing rows
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            # Insert bookings
            if bookings:
                for booking in bookings:
                    booking_list = list(booking)
                    booking_list[7] = f"₹{booking[7]:.2f}"
                    self.tree.insert("", tk.END, values=tuple(booking_list))
                
                self.info_label.config(
                    text=f"✅ {len(bookings)} pending booking(s) found. Click on a booking to see available drivers.",
                    bg="#d4edda",
                    fg="#155724"
                )
            else:
                self.info_label.config(
                    text="⚠ No pending bookings available. All bookings are assigned!",
                    bg="#f8d7da",
                    fg="#721c24"
                )
                
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error loading bookings: {err}")
        finally:
            if conn:
                conn.close()

    def on_booking_select(self, event):
        """Load matching drivers when a booking is selected"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        booking_values = self.tree.item(selected_item, "values")
        booking_id = booking_values[0]
        vehicle_type = booking_values[6]
        
        self.info_label.config(
            text=f"📌 Booking #{booking_id} selected ({vehicle_type} required). Select a driver from dropdown below.",
            bg="#cce5ff",
            fg="#004085"
        )
        
        self.load_drivers(vehicle_type)

    def load_drivers(self, vehicle_type=None):
        """Load available drivers into the Combobox"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if vehicle_type:
                query = """
                    SELECT driver_id, name, vehicle_type, vehicle_number 
                    FROM drivers 
                    WHERE status = 'available' AND vehicle_type = ?
                    ORDER BY name
                """
                cursor.execute(query, (vehicle_type,))
            else:
                query = """
                    SELECT driver_id, name, vehicle_type, vehicle_number 
                    FROM drivers 
                    WHERE status = 'available'
                    ORDER BY vehicle_type, name
                """
                cursor.execute(query)
            
            drivers = cursor.fetchall()
            
            if drivers:
                driver_list = [
                    f"ID:{driver[0]} - {driver[1]} ({driver[2]}, {driver[3]})" 
                    for driver in drivers
                ]
                self.driver_combobox['values'] = driver_list
                self.driver_combobox.current(0)
                
                self.info_label.config(
                    text=f"✅ {len(drivers)} available driver(s) found. Select one and click ASSIGN button below.",
                    bg="#d1ecf1",
                    fg="#0c5460"
                )
            else:
                self.driver_combobox['values'] = []
                self.driver_combobox.set('')
                
                messagebox.showwarning(
                    "No Drivers Available",
                    f"⚠️ No available {vehicle_type} drivers found!\n\n"
                    f"Please register a new {vehicle_type} driver first:\n"
                    f"Admin Dashboard → Register Driver"
                )
                
                self.info_label.config(
                    text=f"⚠ No available {vehicle_type} drivers. Register a driver first!",
                    bg="#f8d7da",
                    fg="#721c24"
                )
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error loading drivers: {err}")
        finally:
            if conn:
                conn.close()

    def check_driver_overlap(self, driver_id, booking_date, booking_time, booking_id=None):
        """
        CRITICAL: Check if driver has overlapping bookings
        Assignment requirement: "Ensure no two bookings overlap for the same driver"
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Query to find overlapping bookings for the same driver on the same date
            query = """
                SELECT booking_id, pickup_location, dropoff_location, pickup_time
                FROM bookings
                WHERE driver_id = ? 
                AND booking_date = ?
                AND status NOT IN ('cancelled', 'completed')
            """
            
            params = [driver_id, booking_date]
            
            # If updating an existing booking, exclude it from the check
            if booking_id:
                query += " AND booking_id != ?"
                params.append(booking_id)
            
            cursor.execute(query, params)
            overlapping = cursor.fetchall()
            
            if overlapping:
                # Found overlapping bookings
                conflict_details = "\n".join([
                    f"  • Booking #{b[0]}: {b[1]} → {b[2]} at {b[3]}"
                    for b in overlapping
                ])
                return False, f"Driver already has booking(s) on {booking_date}:\n{conflict_details}"
            
            return True, "No conflicts"
            
        except sqlite3.Error as err:
            return False, f"Database error: {err}"
        finally:
            if conn:
                conn.close()

    def assign_driver(self):
        """Assign selected driver to selected booking WITH OVERLAP CHECK"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "No Booking Selected", 
                "⚠️ Please select a booking first!\n\n"
                "Click on a row in the bookings table."
            )
            return

        driver_selection = self.driver_combobox.get()
        if not driver_selection:
            messagebox.showerror(
                "No Driver Selected", 
                "⚠️ Please select a driver from the dropdown!"
            )
            return

        # Extract IDs
        driver_id = driver_selection.split(" - ")[0].replace("ID:", "")
        booking_values = self.tree.item(selected_item, "values")
        booking_id = booking_values[0]

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Get booking date and time
            cursor.execute("""
                SELECT booking_date, pickup_time 
                FROM bookings 
                WHERE booking_id = ?
            """, (booking_id,))
            
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Booking not found!")
                return
            
            booking_date = result[0]
            booking_time = result[1]
            
            # CRITICAL: Check for overlapping bookings
            can_assign, message = self.check_driver_overlap(
                driver_id, 
                booking_date, 
                booking_time, 
                booking_id
            )
            
            if not can_assign:
                messagebox.showerror(
                    "❌ Booking Overlap Detected", 
                    f"Cannot assign driver!\n\n{message}\n\n"
                    "⚠️ Assignment requirement:\n"
                    "No two bookings can overlap for the same driver."
                )
                return
            
            # No overlap, proceed with assignment
            cursor.execute(
                "UPDATE bookings SET driver_id = ?, status = 'in_progress' WHERE booking_id = ?",
                (driver_id, booking_id)
            )
            
            cursor.execute(
                "UPDATE drivers SET status = 'busy' WHERE driver_id = ?",
                (driver_id,)
            )
            
            conn.commit()
            
            messagebox.showinfo(
                "✅ Success!", 
                f"Driver assigned successfully!\n\n"
                f"Booking ID: {booking_id}\n"
                f"Driver: {driver_selection.split(' - ')[1].split(' (')[0]}\n"
                f"Date: {booking_date}\n"
                f"Status: In Progress\n\n"
                f"✓ No booking overlaps detected"
            )
            
            # Refresh
            self.load_bookings()
            self.driver_combobox.set('')
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn:
                conn.close()

    def back_to_dashboard(self):
        """Close window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ManageBookingsPage(root)
    root.mainloop()