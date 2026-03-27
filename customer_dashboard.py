import tkinter as tk
from tkinter import messagebox
from booking import BookingPage
from view_bookings import ViewBookingsPage
from cancel_booking import CancelBookingPage
from update_booking import UpdateBookingPage


class CustomerDashboard:
    """Main dashboard for customers."""

    def __init__(self, root, customer_email, customer_name, customer_id):
        self.root = root
        self.customer_email = customer_email
        self.customer_name = customer_name
        self.customer_id = customer_id

        self.root.title("Customer Dashboard")
        
        # FULLSCREEN/MAXIMIZED
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
            text="Customer Dashboard",
            font=("Helvetica", 25, "bold"),
            bg="#DDC01A",
            fg="white",
        ).pack(pady=20)

        # Main Content Section
        main_frame = tk.Frame(self.root, bg="#ffffff", pady=20, padx=20, bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Display Customer Information
        tk.Label(main_frame, text=f"Customer Name: {self.customer_name}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(main_frame, text=f"Customer ID: {self.customer_id}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(main_frame, text=f"Customer Email: {self.customer_email}", font=("Helvetica", 14)).pack(pady=10)

        # Book a Ride Button
        book_button = tk.Button(
            main_frame,
            text="🚖 Book a Ride",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.book_ride
        )
        book_button.pack(pady=10)

        # View Bookings Button
        view_button = tk.Button(
            main_frame,
            text="📋 View Bookings",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.view_bookings
        )
        view_button.pack(pady=10)

        # Update Booking Button
        update_button = tk.Button(
            main_frame,
            text="✏️ Update Booking",
            bg="#17a2b8",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.update_booking
        )
        update_button.pack(pady=10)

        # Cancel Booking Button
        cancel_button = tk.Button(
            main_frame,
            text="❌ Cancel Booking",
            bg="#dc3545",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.cancel_booking
        )
        cancel_button.pack(pady=10)

        # Logout Button
        logout_button = tk.Button(
            main_frame,
            text="🚪 Logout",
            bg="#000000",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.logout
        )
        logout_button.pack(pady=10)

        # Footer Section
        footer_frame = tk.Frame(self.root, bg="#DDC01A", height=60)
        footer_frame.pack(side="bottom", fill="x")

        tk.Label(
            footer_frame,
            text=f"Name: {self.customer_name} | UID: {self.customer_id}",
            font=("Helvetica", 12, "italic"),
            bg="#DDC01A",
            fg="white",
        ).pack(pady=10)

    def book_ride(self):
        """Opens the booking page"""
        booking_window = tk.Toplevel(self.root)
        BookingPage(booking_window, self.customer_id)

    def view_bookings(self):
        """Opens view bookings page"""
        view_booking_window = tk.Toplevel(self.root)
        ViewBookingsPage(view_booking_window, self.customer_id)

    def update_booking(self):
        """Opens update booking page"""
        update_booking_window = tk.Toplevel(self.root)
        UpdateBookingPage(update_booking_window, self.customer_id)

    def cancel_booking(self):
        """Opens cancel booking page"""
        cancel_booking_window = tk.Toplevel(self.root)
        CancelBookingPage(cancel_booking_window, self.customer_id)

    def logout(self):
        """Logs the customer out"""
        self.root.destroy()
        from login import LoginPage
        new_root = tk.Tk()
        LoginPage(new_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerDashboard(root, "customer@example.com", "John Doe", 1)
    root.mainloop()