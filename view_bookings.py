import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH


class ViewBookingsPage:

    def __init__(self, root, customer_id):
        self.root = root
        self.customer_id = customer_id
        self.root.title("View Bookings")
        self.root.geometry("1400x600")
        self.root.configure(bg="#f5f5f5")
        
        self.current_filter = "all"  # Track current filter

        # Header Label
        header_label = tk.Label(
            self.root,
            text="My Booking Records",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 18, "bold"),
            pady=10
        )
        header_label.pack(fill="x")

        # Filter Buttons Frame
        filter_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        filter_frame.pack(fill="x", padx=20)

        tk.Label(
            filter_frame,
            text="Filter:",
            font=("Helvetica", 12, "bold"),
            bg="#f5f5f5"
        ).pack(side="left", padx=5)

        # All Bookings Button
        self.all_button = tk.Button(
            filter_frame,
            text="📋 All Bookings",
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=15,
            relief="raised",
            bd=3,
            command=self.show_all_bookings
        )
        self.all_button.pack(side="left", padx=5)

        # History Button (Completed only)
        self.history_button = tk.Button(
            filter_frame,
            text="✅ History (Completed)",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=18,
            relief="flat",
            command=self.show_history
        )
        self.history_button.pack(side="left", padx=5)

        # Pending Button
        self.pending_button = tk.Button(
            filter_frame,
            text="⏳ Pending",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.show_pending
        )
        self.pending_button.pack(side="left", padx=5)

        # In Progress Button
        self.progress_button = tk.Button(
            filter_frame,
            text="🚗 In Progress",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.show_in_progress
        )
        self.progress_button.pack(side="left", padx=5)

        # Cancelled Button
        self.cancelled_button = tk.Button(
            filter_frame,
            text="❌ Cancelled",
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            relief="flat",
            command=self.show_cancelled
        )
        self.cancelled_button.pack(side="left", padx=5)

        # Treeview Frame
        tree_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview for displaying bookings
        columns = ("booking_id", "pickup", "dropoff", "date", "time", "vehicle", "distance", "fare", "driver", "status", "payment")
        self.booking_tree = ttk.Treeview(
            tree_frame, 
            columns=columns,
            show="headings", 
            height=20
        )

        # Define columns
        self.booking_tree.heading("booking_id", text="ID")
        self.booking_tree.heading("pickup", text="Pickup Location")
        self.booking_tree.heading("dropoff", text="Dropoff Location")
        self.booking_tree.heading("date", text="Date")
        self.booking_tree.heading("time", text="Time")
        self.booking_tree.heading("vehicle", text="Vehicle")
        self.booking_tree.heading("distance", text="Distance (km)")
        self.booking_tree.heading("fare", text="Fare (₹)")
        self.booking_tree.heading("driver", text="Driver Assigned")
        self.booking_tree.heading("status", text="Status")
        self.booking_tree.heading("payment", text="Payment")

        self.booking_tree.column("booking_id", anchor="center", width=50)
        self.booking_tree.column("pickup", anchor="w", width=130)
        self.booking_tree.column("dropoff", anchor="w", width=130)
        self.booking_tree.column("date", anchor="center", width=90)
        self.booking_tree.column("time", anchor="center", width=60)
        self.booking_tree.column("vehicle", anchor="center", width=90)
        self.booking_tree.column("distance", anchor="center", width=100)
        self.booking_tree.column("fare", anchor="center", width=80)
        self.booking_tree.column("driver", anchor="w", width=120)
        self.booking_tree.column("status", anchor="center", width=100)
        self.booking_tree.column("payment", anchor="center", width=80)

        # Scrollbar
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical", command=self.booking_tree.yview)
        self.booking_tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.booking_tree.pack(fill="both", expand=True)

        # Summary Frame
        summary_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        summary_frame.pack(fill="x", padx=20)

        self.summary_label = tk.Label(
            summary_frame,
            text="Total bookings: 0 | Total spent: ₹0.00",
            font=("Helvetica", 12, "bold"),
            bg="#f0f0f0",
            fg="#000000"
        )
        self.summary_label.pack()

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        button_frame.pack(fill="x", padx=20)

        # Refresh Button
        refresh_button = tk.Button(
            button_frame,
            text="🔄 Refresh",
            bg="#28a745",
            fg="white",
            font=("Helvetica", 12),
            width=15,
            relief="flat",
            command=self.refresh_current_view
        )
        refresh_button.pack(side="left", padx=10)

        # Back Button
        back_button = tk.Button(
            button_frame,
            text="← Back to Dashboard",
            bg="#000000",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            relief="flat",
            command=self.back_to_dashboard
        )
        back_button.pack(side="left", padx=10)

        # Load Data
        self.load_bookings()

    def update_button_styles(self, active_button):
        """Update button styles to show which filter is active"""
        buttons = {
            "all": self.all_button,
            "history": self.history_button,
            "pending": self.pending_button,
            "progress": self.progress_button,
            "cancelled": self.cancelled_button
        }
        
        for key, button in buttons.items():
            if key == active_button:
                button.config(bg="#007bff", relief="raised", bd=3, font=("Helvetica", 12, "bold"))
            else:
                button.config(bg="#6c757d", relief="flat", bd=1, font=("Helvetica", 12))

    def show_all_bookings(self):
        """Show all bookings"""
        self.current_filter = "all"
        self.update_button_styles("all")
        self.load_bookings()

    def show_history(self):
        """Show only completed bookings"""
        self.current_filter = "completed"
        self.update_button_styles("history")
        self.load_bookings(status_filter="completed")

    def show_pending(self):
        """Show only pending bookings"""
        self.current_filter = "pending"
        self.update_button_styles("pending")
        self.load_bookings(status_filter="pending")

    def show_in_progress(self):
        """Show only in-progress bookings"""
        self.current_filter = "in_progress"
        self.update_button_styles("progress")
        self.load_bookings(status_filter=["in_progress", "accepted", "started"])

    def show_cancelled(self):
        """Show only cancelled bookings"""
        self.current_filter = "cancelled"
        self.update_button_styles("cancelled")
        self.load_bookings(status_filter="cancelled")

    def refresh_current_view(self):
        """Refresh current filter view"""
        if self.current_filter == "all":
            self.show_all_bookings()
        elif self.current_filter == "completed":
            self.show_history()
        elif self.current_filter == "pending":
            self.show_pending()
        elif self.current_filter == "in_progress":
            self.show_in_progress()
        elif self.current_filter == "cancelled":
            self.show_cancelled()

    def load_bookings(self, status_filter=None):
        """Load customer bookings from database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if status_filter:
                if isinstance(status_filter, list):
                    placeholders = ','.join('?' * len(status_filter))
                    query = f"""
                        SELECT b.booking_id, b.pickup_location, b.dropoff_location, b.booking_date, 
                               substr(b.pickup_time, 12, 5) as time,
                               b.vehicle_type,
                               b.distance,
                               b.fare,
                               COALESCE(d.name, 'Not Assigned') as driver_name,
                               b.status, b.payment_type
                        FROM bookings b
                        LEFT JOIN drivers d ON b.driver_id = d.driver_id
                        WHERE b.customer_id = ? AND b.status IN ({placeholders})
                        ORDER BY b.booking_id DESC
                    """
                    cursor.execute(query, (self.customer_id, *status_filter))
                else:
                    query = """
                        SELECT b.booking_id, b.pickup_location, b.dropoff_location, b.booking_date, 
                               substr(b.pickup_time, 12, 5) as time,
                               b.vehicle_type,
                               b.distance,
                               b.fare,
                               COALESCE(d.name, 'Not Assigned') as driver_name,
                               b.status, b.payment_type
                        FROM bookings b
                        LEFT JOIN drivers d ON b.driver_id = d.driver_id
                        WHERE b.customer_id = ? AND b.status = ?
                        ORDER BY b.booking_id DESC
                    """
                    cursor.execute(query, (self.customer_id, status_filter))
            else:
                query = """
                    SELECT b.booking_id, b.pickup_location, b.dropoff_location, b.booking_date, 
                           substr(b.pickup_time, 12, 5) as time,
                           b.vehicle_type,
                           b.distance,
                           b.fare,
                           COALESCE(d.name, 'Not Assigned') as driver_name,
                           b.status, b.payment_type
                    FROM bookings b
                    LEFT JOIN drivers d ON b.driver_id = d.driver_id
                    WHERE b.customer_id = ?
                    ORDER BY b.booking_id DESC
                """
                cursor.execute(query, (self.customer_id,))
            
            rows = cursor.fetchall()

            # Clear existing rows
            for item in self.booking_tree.get_children():
                self.booking_tree.delete(item)

            # Calculate totals
            total_bookings = len(rows)
            total_spent = sum(row[7] for row in rows if row[7])

            # Insert rows
            if rows:
                for row in rows:
                    # Format the row data
                    formatted_row = list(row)
                    formatted_row[6] = f"{row[6]:.1f}" if row[6] else "N/A"  # Distance
                    formatted_row[7] = f"₹{row[7]:.2f}" if row[7] else "₹0.00"  # Fare
                    self.booking_tree.insert("", "end", values=tuple(formatted_row))
                
                # Update summary
                filter_text = ""
                if status_filter:
                    if isinstance(status_filter, list):
                        filter_text = " (In Progress/Active)"
                    else:
                        filter_text = f" ({status_filter.title()})"
                
                self.summary_label.config(
                    text=f"Total bookings{filter_text}: {total_bookings} | Total spent: ₹{total_spent:.2f}"
                )
            else:
                filter_msg = ""
                if status_filter:
                    if isinstance(status_filter, list):
                        filter_msg = "in progress/active"
                    else:
                        filter_msg = status_filter
                    messagebox.showinfo("No Bookings", f"You have no {filter_msg} bookings.")
                else:
                    messagebox.showinfo("No Bookings", "You have no bookings yet.")
                
                self.summary_label.config(text="Total bookings: 0 | Total spent: ₹0.00")

        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error fetching bookings: {err}")
        finally:
            if conn:
                conn.close()

    def back_to_dashboard(self):
        """Close current window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ViewBookingsPage(root, 1)
    root.mainloop()
    