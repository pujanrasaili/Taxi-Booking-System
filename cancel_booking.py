import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_PATH


class CancelBookingPage:

    def __init__(self, root, customer_id):
        self.root = root
        self.customer_id = customer_id
        self.root.title("Cancel Booking")
        self.root.geometry("400x300")
        self.root.configure(bg="#000000")

        # Header Label
        header_label = tk.Label(
            self.root,
            text="Cancel a Booking",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 25, "bold"),
            pady=10
        )
        header_label.pack(fill="x")

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#ffffff", pady=20, padx=20, bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Booking ID Label and Dropdown
        tk.Label(main_frame, text="Select Booking ID:", bg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky="w")
        
        self.booking_id_var = tk.StringVar()
        self.booking_dropdown = ttk.Combobox(
            main_frame, 
            textvariable=self.booking_id_var, 
            font=("Helvetica", 12), 
            state="readonly",
            width=20
        )
        self.booking_dropdown.grid(row=0, column=1, pady=10, padx=10)
        self.load_bookings()

        # Cancel Button
        cancel_button = tk.Button(
            main_frame,
            text="Cancel Booking",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 12),
            width=15,
            relief="flat",
            command=self.cancel_booking
        )
        cancel_button.grid(row=1, column=0, columnspan=2, pady=20)

        # Back Button
        back_button = tk.Button(
            main_frame,
            text="Back",
            bg="#000000",
            fg="white",
            font=("Helvetica", 12),
            width=15,
            relief="flat",
            command=self.back_to_dashboard
        )
        back_button.grid(row=2, column=0, columnspan=2, pady=10)

    def load_bookings(self):
        """Load all cancellable bookings for this customer"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Only load bookings that are pending or in_progress (not started/completed/cancelled)
            query = """
                SELECT booking_id, pickup_location, dropoff_location, status
                FROM bookings 
                WHERE customer_id = ? AND status IN ('pending', 'in_progress', 'accepted')
            """
            cursor.execute(query, (self.customer_id,))
            bookings = cursor.fetchall()
            
            # Format as "ID: Pickup -> Dropoff (Status)"
            booking_list = [f"{b[0]}: {b[1]} → {b[2]} ({b[3]})" for b in bookings]
            self.booking_dropdown['values'] = booking_list

        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error fetching bookings: {err}")
        finally:
            if conn:
                conn.close()

    def cancel_booking(self):
        """Cancel the selected booking"""
        booking_selection = self.booking_id_var.get()

        if not booking_selection:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return

        # Extract booking ID and status from selection
        booking_id = booking_selection.split(":")[0]
        
        # Check if trip has started
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT status FROM bookings WHERE booking_id = ?", (booking_id,))
            result = cursor.fetchone()
            
            if result:
                status = result[0]
                if status in ['started', 'completed', 'cancelled']:
                    messagebox.showerror("Cannot Cancel", f"Cannot cancel booking. Trip is already {status}.")
                    return
            
            # Confirm cancellation
            confirm = messagebox.askyesno("Confirm Cancellation", 
                                         f"Are you sure you want to cancel Booking ID {booking_id}?")
            if not confirm:
                return
            
            # Cancel the booking
            query = "UPDATE bookings SET status = 'cancelled' WHERE booking_id = ?"
            cursor.execute(query, (booking_id,))
            conn.commit()

            messagebox.showinfo("Success", f"Booking ID {booking_id} has been successfully cancelled.")
            self.load_bookings()  # Refresh the dropdown

        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error cancelling booking: {err}")
        finally:
            if conn:
                conn.close()

    def back_to_dashboard(self):
        """Close current window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CancelBookingPage(root, 1)
    root.mainloop()