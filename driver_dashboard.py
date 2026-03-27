import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH


class AssignedTripsViewer:
    """View assigned trips for a driver"""

    def __init__(self, root, driver_id):
        self.root = root
        self.driver_id = driver_id
        self.root.title("Assigned Trips")
        
        # ✅ FULLSCREEN FOR POPUP WINDOWS
        self.root.state('zoomed')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#f5f5f5")
        
        self.current_filter = "all"

        # Header Section
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=80)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame,
            text="My Assigned Trips",
            font=("Helvetica", 25, "bold"),
            bg="#DDC01A",
            fg="white",
        ).pack(pady=20)

        # Filter Buttons Frame
        filter_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        filter_frame.pack(fill="x", padx=20)

        tk.Label(
            filter_frame,
            text="Filter:",
            font=("Helvetica", 12, "bold"),
            bg="#f5f5f5"
        ).pack(side="left", padx=5)

        # All Trips Button
        self.all_button = tk.Button(
            filter_frame,
            text="📋 All Trips",
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15,
            relief="raised",
            bd=3,
            command=self.show_all_trips
        )
        self.all_button.pack(side="left", padx=5)

        # New Assigned Button
        self.new_button = tk.Button(
            filter_frame,
            text="🆕 New (In Progress)",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=18,
            relief="flat",
            command=self.show_new_trips
        )
        self.new_button.pack(side="left", padx=5)

        # Accepted Button
        self.accepted_button = tk.Button(
            filter_frame,
            text="✅ Accepted",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.show_accepted
        )
        self.accepted_button.pack(side="left", padx=5)

        # Started Button
        self.started_button = tk.Button(
            filter_frame,
            text="🚗 Started",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.show_started
        )
        self.started_button.pack(side="left", padx=5)

        # Completed Button
        self.completed_button = tk.Button(
            filter_frame,
            text="✔️ Completed",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.show_completed
        )
        self.completed_button.pack(side="left", padx=5)

        # Main Content Section
        content_frame = tk.Frame(self.root, bg="white", pady=20, padx=20)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview Table
        columns = ("booking_id", "customer", "pickup_location", "dropoff_location", "date", "time", "vehicle", "distance", "fare", "status")
        self.trip_table = ttk.Treeview(
            content_frame,
            columns=columns,
            show="headings",
        )
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=30)

        # Define columns
        self.trip_table.heading("booking_id", text="Booking ID")
        self.trip_table.heading("customer", text="Customer")
        self.trip_table.heading("pickup_location", text="Pickup Location")
        self.trip_table.heading("dropoff_location", text="Dropoff Location")
        self.trip_table.heading("date", text="Date")
        self.trip_table.heading("time", text="Time")
        self.trip_table.heading("vehicle", text="Vehicle")
        self.trip_table.heading("distance", text="Distance (km)")
        self.trip_table.heading("fare", text="Fare (₹)")
        self.trip_table.heading("status", text="Status")

        self.trip_table.column("booking_id", width=100, anchor="center")
        self.trip_table.column("customer", width=120, anchor="w")
        self.trip_table.column("pickup_location", width=150, anchor="w")
        self.trip_table.column("dropoff_location", width=150, anchor="w")
        self.trip_table.column("date", width=100, anchor="center")
        self.trip_table.column("time", width=80, anchor="center")
        self.trip_table.column("vehicle", width=90, anchor="center")
        self.trip_table.column("distance", width=100, anchor="center")
        self.trip_table.column("fare", width=90, anchor="center")
        self.trip_table.column("status", width=120, anchor="center")

        self.trip_table.pack(fill="both", expand=True)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(content_frame, orient="vertical", command=self.trip_table.yview)
        scrollbar_x = ttk.Scrollbar(content_frame, orient="horizontal", command=self.trip_table.xview)
        self.trip_table.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # Summary Frame
        summary_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        summary_frame.pack(fill="x", padx=20)

        self.summary_label = tk.Label(
            summary_frame,
            text="Total trips: 0 | Total earnings: ₹0.00",
            font=("Helvetica", 12, "bold"),
            bg="#f0f0f0",
            fg="#000000"
        )
        self.summary_label.pack()

        # Action Buttons Frame
        action_frame = tk.Frame(self.root, bg="#f5f5f5", pady=15)
        action_frame.pack(fill="x", padx=20)

        # Accept Button
        accept_btn = tk.Button(
            action_frame,
            text="✓ Accept Trip",
            bg="#28a745",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15,
            relief="flat",
            command=self.accept_trip
        )
        accept_btn.pack(side="left", padx=10)

        # Start Button
        start_btn = tk.Button(
            action_frame,
            text="▶ Start Trip",
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15,
            relief="flat",
            command=self.start_trip
        )
        start_btn.pack(side="left", padx=10)

        # Complete Button
        complete_btn = tk.Button(
            action_frame,
            text="✓ Complete Trip",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15,
            relief="flat",
            command=self.complete_trip
        )
        complete_btn.pack(side="left", padx=10)

        # Reject Button
        reject_btn = tk.Button(
            action_frame,
            text="✖ Reject Trip",
            bg="#dc3545",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15,
            relief="flat",
            command=self.reject_trip
        )
        reject_btn.pack(side="left", padx=10)

        # Refresh Button
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Refresh",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=12,
            relief="flat",
            command=self.refresh_current_view
        )
        refresh_btn.pack(side="left", padx=10)

        # Back Button
        back_btn = tk.Button(
            action_frame,
            text="← Back",
            bg="#000000",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.back_to_dashboard
        )
        back_btn.pack(side="left", padx=10)

        # Load trips
        self.load_assigned_trips()

    def update_button_styles(self, active_button):
        """Update button styles"""
        buttons = {
            "all": self.all_button,
            "new": self.new_button,
            "accepted": self.accepted_button,
            "started": self.started_button,
            "completed": self.completed_button
        }
        
        for key, button in buttons.items():
            if key == active_button:
                button.config(bg="#007bff", relief="raised", bd=3, font=("Helvetica", 12, "bold"))
            else:
                button.config(bg="#6c757d", relief="flat", bd=1, font=("Helvetica", 12))

    def show_all_trips(self):
        self.current_filter = "all"
        self.update_button_styles("all")
        self.load_assigned_trips()

    def show_new_trips(self):
        self.current_filter = "in_progress"
        self.update_button_styles("new")
        self.load_assigned_trips(status_filter="in_progress")

    def show_accepted(self):
        self.current_filter = "accepted"
        self.update_button_styles("accepted")
        self.load_assigned_trips(status_filter="accepted")

    def show_started(self):
        self.current_filter = "started"
        self.update_button_styles("started")
        self.load_assigned_trips(status_filter="started")

    def show_completed(self):
        self.current_filter = "completed"
        self.update_button_styles("completed")
        self.load_assigned_trips(status_filter="completed")

    def refresh_current_view(self):
        if self.current_filter == "all":
            self.show_all_trips()
        elif self.current_filter == "in_progress":
            self.show_new_trips()
        elif self.current_filter == "accepted":
            self.show_accepted()
        elif self.current_filter == "started":
            self.show_started()
        elif self.current_filter == "completed":
            self.show_completed()

    def load_assigned_trips(self, status_filter=None):
        """Fetch and display trips"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            if status_filter:
                query = """
                    SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location, 
                           b.booking_date, substr(b.pickup_time, 12, 5) as time,
                           b.vehicle_type, b.distance, b.fare, b.status
                    FROM bookings b
                    JOIN customers c ON b.customer_id = c.customer_id
                    WHERE b.driver_id = ? AND b.status = ?
                    ORDER BY b.booking_date DESC, b.pickup_time DESC
                """
                cursor.execute(query, (self.driver_id, status_filter))
            else:
                query = """
                    SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location, 
                           b.booking_date, substr(b.pickup_time, 12, 5) as time,
                           b.vehicle_type, b.distance, b.fare, b.status
                    FROM bookings b
                    JOIN customers c ON b.customer_id = c.customer_id
                    WHERE b.driver_id = ?
                    ORDER BY b.booking_date DESC, b.pickup_time DESC
                """
                cursor.execute(query, (self.driver_id,))
            
            trips = cursor.fetchall()

            for row in self.trip_table.get_children():
                self.trip_table.delete(row)

            total_trips = len(trips)
            total_earnings = sum(trip[8] for trip in trips if trip[8])

            if trips:
                for trip in trips:
                    formatted_trip = list(trip)
                    formatted_trip[7] = f"{trip[7]:.1f}" if trip[7] else "N/A"
                    formatted_trip[8] = f"₹{trip[8]:.2f}" if trip[8] else "₹0.00"
                    self.trip_table.insert("", "end", values=tuple(formatted_trip))
                
                filter_text = ""
                if status_filter:
                    filter_text = f" ({status_filter.replace('_', ' ').title()})"
                
                self.summary_label.config(
                    text=f"Total trips{filter_text}: {total_trips} | Total earnings: ₹{total_earnings:.2f}"
                )
            else:
                filter_msg = ""
                if status_filter:
                    filter_msg = f" in '{status_filter.replace('_', ' ')}' status"
                messagebox.showinfo("No Trips", f"No trips assigned to you{filter_msg}.")
                self.summary_label.config(text="Total trips: 0 | Total earnings: ₹0.00")

        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        finally:
            if conn:
                conn.close()

    def get_selected_booking(self):
        """Get selected booking"""
        selected = self.trip_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a trip first.")
            return None, None
        
        values = self.trip_table.item(selected[0])['values']
        return values[0], values[9]

    def accept_trip(self):
        """Accept trip"""
        booking_id, status = self.get_selected_booking()
        if not booking_id:
            return
        
        if status != "in_progress":
            messagebox.showwarning("Invalid Action", "Only trips with 'in_progress' status can be accepted.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE bookings SET status = 'accepted' WHERE booking_id = ?", (booking_id,))
            conn.commit()
            
            messagebox.showinfo("Success", f"Trip {booking_id} accepted successfully!")
            self.refresh_current_view()
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn:
                conn.close()

    def start_trip(self):
        """Start trip"""
        booking_id, status = self.get_selected_booking()
        if not booking_id:
            return
        
        if status != "accepted":
            messagebox.showwarning("Invalid Action", "Only accepted trips can be started.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE bookings SET status = 'started' WHERE booking_id = ?", (booking_id,))
            conn.commit()
            
            messagebox.showinfo("Success", f"Trip {booking_id} started!")
            self.refresh_current_view()
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn:
                conn.close()

    def complete_trip(self):
        """Complete trip"""
        booking_id, status = self.get_selected_booking()
        if not booking_id:
            return
        
        if status != "started":
            messagebox.showwarning("Invalid Action", "Only started trips can be completed.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE bookings SET status = 'completed' WHERE booking_id = ?", (booking_id,))
            cursor.execute("UPDATE drivers SET status = 'available' WHERE driver_id = ?", (self.driver_id,))
            conn.commit()
            
            messagebox.showinfo("Success", f"Trip {booking_id} completed!")
            self.refresh_current_view()
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn:
                conn.close()

    def reject_trip(self):
        """Reject trip"""
        booking_id, status = self.get_selected_booking()
        if not booking_id:
            return
        
        if status in ["completed", "cancelled"]:
            messagebox.showwarning("Invalid Action", "Cannot reject completed or cancelled trips.")
            return

        confirm = messagebox.askyesno("Confirm", f"Reject trip {booking_id}?")
        if not confirm:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE bookings SET status = 'pending', driver_id = NULL WHERE booking_id = ?", (booking_id,))
            cursor.execute("UPDATE drivers SET status = 'available' WHERE driver_id = ?", (self.driver_id,))
            conn.commit()
            
            messagebox.showinfo("Success", f"Trip {booking_id} rejected.")
            self.refresh_current_view()
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn:
                conn.close()

    def back_to_dashboard(self):
        """Close window"""
        self.root.destroy()


class DriverDashboard:
    """Main dashboard for drivers"""

    def __init__(self, root, driver_email, driver_name, driver_id):
        self.root = root
        self.driver_email = driver_email
        self.driver_name = driver_name
        self.driver_id = driver_id

        self.root.title("Driver Dashboard")
        
        # ✅ FULLSCREEN FOR MAIN DASHBOARD
        self.root.state('zoomed')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#000000")

        # Header Section
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=80)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame,
            text="Driver Dashboard",
            font=("Helvetica", 25, "bold"),
            bg="#DDC01A",
            fg="white",
        ).pack(pady=20)

        # Main Content Section
        main_frame = tk.Frame(self.root, bg="#ffffff", pady=20, padx=20, bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Driver Info
        tk.Label(main_frame, text=f"Driver Name: {self.driver_name}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(main_frame, text=f"Driver ID: {self.driver_id}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(main_frame, text=f"Driver Email: {self.driver_email}", font=("Helvetica", 14)).pack(pady=10)

        # View Assigned Trips Button
        trips_button = tk.Button(
            main_frame,
            text="🚗 View My Trips",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=25,
            relief="flat",
            command=self.view_assigned_trips,
            padx=20,
            pady=10
        )
        trips_button.pack(pady=15)

        # Logout Button
        logout_button = tk.Button(
            main_frame,
            text="Logout",
            bg="#000000",
            fg="white",
            font=("Helvetica", 14),
            width=25,
            relief="flat",
            command=self.logout,
            padx=20,
            pady=10
        )
        logout_button.pack(pady=10)

    def view_assigned_trips(self):
        """Open assigned trips viewer"""
        view_window = tk.Toplevel(self.root)
        AssignedTripsViewer(view_window, driver_id=self.driver_id)

    def logout(self):
        """Logout"""
        self.root.destroy()
        from login import LoginPage
        new_root = tk.Tk()
        LoginPage(new_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = DriverDashboard(root, "driver@example.com", "John Doe", 1)
    root.mainloop()