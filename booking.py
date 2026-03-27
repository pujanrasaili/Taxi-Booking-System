import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from config import DB_PATH, COLORS
from fare_calculator import FareCalculator
from validation_utils import ValidationUtils  # NEW IMPORT


class BookingPage:

    def __init__(self, root, customer_id):
        self.root = root
        self.customer_id = customer_id
        self.root.title("Book a Taxi")
        self.root.geometry("600x900")
        self.root.configure(bg="#000000")
        
        self.estimated_fare = 0
        self.estimated_distance = 0

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=80)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        header_label = tk.Label(
            header_frame,
            text="Book Your Taxi",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 16, "bold")
        )
        header_label.pack(expand=True)

        # Scrollable container
        container = tk.Frame(self.root, bg="#000000")
        container.pack(side="top", fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#000000", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
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

        # Main Frame
        main_frame = tk.Frame(scrollable_frame, bg="#ffffff", pady=20, padx=20, bd=2, relief="groove")
        main_frame.pack(pady=20, padx=20)

        # From Entry
        tk.Label(main_frame, text="From (Pickup Location):", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.from_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35)
        self.from_entry.pack(pady=5)

        # To Entry
        tk.Label(main_frame, text="To (Drop-off Location):", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.to_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=35)
        self.to_entry.pack(pady=5)
        
        # Vehicle Type
        tk.Label(main_frame, text="Select Vehicle Type:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.vehicle_type_var = tk.StringVar(value="Sedan")
        
        vehicle_frame = tk.Frame(main_frame, bg="#ffffff")
        vehicle_frame.pack(pady=5, fill="x")
        
        vehicles = ["Sedan", "SUV", "Hatchback", "Van", "Bike"]
        for vehicle in vehicles:
            rb = tk.Radiobutton(
                vehicle_frame,
                text=vehicle,
                variable=self.vehicle_type_var,
                value=vehicle,
                bg="#ffffff",
                font=("Helvetica", 10),
                command=self.calculate_fare
            )
            rb.pack(side="left", padx=5)

        # Booking Date
        tk.Label(main_frame, text="Select Booking Date:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.calendar = Calendar(main_frame, font=("Helvetica", 12), selectmode='day')
        self.calendar.pack(pady=5)

        # Booking Time
        tk.Label(main_frame, text="Select Booking Time (HH:MM):", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        time_frame = tk.Frame(main_frame, bg="#ffffff")
        time_frame.pack(pady=5)

        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")

        hours = [f"{h:02}" for h in range(24)]
        minutes = [f"{m:02}" for m in range(0, 60, 5)]

        tk.Label(time_frame, text="Hour:", bg="#ffffff", font=("Helvetica", 10)).grid(row=0, column=0)
        hour_dropdown = tk.OptionMenu(time_frame, self.hour_var, *hours)
        hour_dropdown.grid(row=0, column=1)

        tk.Label(time_frame, text="Minute:", bg="#ffffff", font=("Helvetica", 10)).grid(row=0, column=2)
        minute_dropdown = tk.OptionMenu(time_frame, self.minute_var, *minutes)
        minute_dropdown.grid(row=0, column=3)

        # Calculate Fare Button
        estimate_button = tk.Button(
            main_frame,
            text="💰 Calculate Fare",
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            relief="flat",
            command=self.calculate_fare
        )
        estimate_button.pack(pady=10)
        
        # Fare Display Frame
        self.fare_frame = tk.Frame(main_frame, bg="#f0f0f0", bd=2, relief="groove")
        self.fare_frame.pack(pady=10, fill="x", padx=10)
        
        self.fare_label = tk.Label(
            self.fare_frame,
            text="📍 Enter locations and click 'Calculate Fare'",
            bg="#f0f0f0",
            font=("Helvetica", 11),
            fg="#666666"
        )
        self.fare_label.pack(pady=10)

        # Payment Type
        tk.Label(main_frame, text="Payment Type:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.payment_type_var = tk.StringVar(value="cash")
        payment_frame = tk.Frame(main_frame, bg="#ffffff")
        payment_frame.pack(pady=5)

        cash_button = tk.Radiobutton(
            payment_frame, text="Cash", variable=self.payment_type_var, value="cash", bg="#ffffff", font=("Helvetica", 10)
        )
        cash_button.grid(row=0, column=0, padx=10)

        online_button = tk.Radiobutton(
            payment_frame, text="Online", variable=self.payment_type_var, value="online", bg="#ffffff", font=("Helvetica", 10)
        )
        online_button.grid(row=0, column=1, padx=10)

        # Confirm Booking Button
        confirm_button = tk.Button(
            main_frame,
            text="Confirm Booking",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 14),
            width=20,
            relief="flat",
            command=self.confirm_booking
        )
        confirm_button.pack(pady=15)

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
        back_button.pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def calculate_fare(self):
        """Calculate and display estimated fare with VALIDATIONS"""
        from_location = self.from_entry.get().strip()
        to_location = self.to_entry.get().strip()
        vehicle_type = self.vehicle_type_var.get()
        
        # ✅ VALIDATION 1: Check locations
        is_valid, error_msg = ValidationUtils.validate_location(from_location, "Pickup location")
        if not is_valid:
            self.fare_label.config(text=error_msg, fg="#dc3545")
            return
        
        is_valid, error_msg = ValidationUtils.validate_location(to_location, "Drop-off location")
        if not is_valid:
            self.fare_label.config(text=error_msg, fg="#dc3545")
            return
        
        # ✅ VALIDATION 2: Check if locations are same
        is_valid, error_msg = ValidationUtils.validate_same_location(from_location, to_location)
        if not is_valid:
            self.fare_label.config(text=error_msg, fg="#dc3545")
            messagebox.showerror("Same Location", error_msg)
            return
        
        try:
            # Get booking time
            booking_date = self.calendar.get_date()
            booking_time = f"{self.hour_var.get()}:{self.minute_var.get()}"
            date_obj = datetime.strptime(booking_date, "%m/%d/%y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            
            # ✅ VALIDATION 3: Check date
            is_valid, error_msg = ValidationUtils.validate_booking_date(formatted_date)
            if not is_valid:
                self.fare_label.config(text=error_msg, fg="#dc3545")
                messagebox.showerror("Invalid Date", error_msg)
                return
            
            # ✅ VALIDATION 4: Check time
            is_valid, error_msg = ValidationUtils.validate_booking_time(formatted_date, booking_time)
            if not is_valid:
                self.fare_label.config(text=error_msg, fg="#dc3545")
                messagebox.showerror("Invalid Time", error_msg)
                return
            
            pickup_datetime = f"{formatted_date} {booking_time}:00"
            pickup_time = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
            
            # Estimate distance
            self.estimated_distance = FareCalculator.estimate_distance(from_location, to_location)
            
            # ✅ VALIDATION 5: Check distance
            is_valid, error_msg = ValidationUtils.validate_distance(self.estimated_distance)
            if not is_valid:
                self.fare_label.config(text=error_msg, fg="#dc3545")
                messagebox.showerror("Invalid Distance", error_msg)
                return
            
            # Calculate fare
            breakdown = FareCalculator.get_fare_breakdown(
                self.estimated_distance,
                vehicle_type,
                pickup_time
            )
            
            self.estimated_fare = breakdown['total']
            
            # ✅ VALIDATION 6: Check fare
            is_valid, error_msg = ValidationUtils.validate_fare(self.estimated_fare)
            if not is_valid:
                self.fare_label.config(text=error_msg, fg="#dc3545")
                messagebox.showerror("Invalid Fare", error_msg)
                return
            
            # Display fare breakdown
            fare_text = f"""
✅ FARE CALCULATED SUCCESSFULLY

Estimated Distance: {self.estimated_distance} km
Vehicle Type: {vehicle_type}
Base Fare: ₹{breakdown['base_fare']}
Distance Fare: ₹{breakdown['distance_fare']} ({breakdown['per_km_rate']}/km)
Subtotal: ₹{breakdown['subtotal']}
Time Factor: {breakdown['multiplier_text']}
━━━━━━━━━━━━━━━━━━━━━━
Total Estimated Fare: ₹{self.estimated_fare}
            """
            
            self.fare_label.config(
                text=fare_text,
                font=("Courier", 10),
                fg="#000000",
                justify="left"
            )
            
        except Exception as e:
            self.fare_label.config(
                text=f"Error calculating fare: {str(e)}",
                fg="#dc3545"
            )

    def confirm_booking(self):
        """Handle booking confirmation with ALL VALIDATIONS"""
        from_location = self.from_entry.get().strip()
        to_location = self.to_entry.get().strip()
        booking_date = self.calendar.get_date()
        booking_time = f"{self.hour_var.get()}:{self.minute_var.get()}"
        payment_type = self.payment_type_var.get()
        vehicle_type = self.vehicle_type_var.get()

        # ✅ VALIDATION 1: Check locations
        is_valid, error_msg = ValidationUtils.validate_location(from_location, "Pickup location")
        if not is_valid:
            messagebox.showerror("Invalid Pickup", error_msg)
            self.from_entry.focus()
            return
        
        is_valid, error_msg = ValidationUtils.validate_location(to_location, "Drop-off location")
        if not is_valid:
            messagebox.showerror("Invalid Dropoff", error_msg)
            self.to_entry.focus()
            return
        
        # ✅ VALIDATION 2: Same location check
        is_valid, error_msg = ValidationUtils.validate_same_location(from_location, to_location)
        if not is_valid:
            messagebox.showerror("Same Location", error_msg)
            return
        
        # ✅ VALIDATION 3: Fare must be calculated
        if self.estimated_fare == 0:
            messagebox.showwarning("Fare Not Calculated", "Please calculate fare before confirming booking.")
            return

        try:
            # Convert date
            date_obj = datetime.strptime(booking_date, "%m/%d/%y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            
            # ✅ VALIDATION 4: Date validation
            is_valid, error_msg = ValidationUtils.validate_booking_date(formatted_date)
            if not is_valid:
                messagebox.showerror("Invalid Date", error_msg)
                return
            
            # ✅ VALIDATION 5: Time validation
            is_valid, error_msg = ValidationUtils.validate_booking_time(formatted_date, booking_time)
            if not is_valid:
                messagebox.showerror("Invalid Time", error_msg)
                return
            
            pickup_datetime = f"{formatted_date} {booking_time}:00"

            # Insert booking
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            query = """
                INSERT INTO bookings (customer_id, pickup_location, dropoff_location, pickup_time, 
                                    booking_date, status, payment_type, fare, distance, vehicle_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                self.customer_id, from_location, to_location, pickup_datetime,
                formatted_date, 'pending', payment_type, self.estimated_fare,
                self.estimated_distance, vehicle_type
            ))
            conn.commit()
            
            messagebox.showinfo(
                "✅ Booking Confirmed!",
                f"Your booking has been confirmed successfully!\n\n"
                f"📍 From: {from_location}\n"
                f"📍 To: {to_location}\n"
                f"📅 Date: {formatted_date}\n"
                f"🕐 Time: {booking_time}\n"
                f"🚗 Vehicle: {vehicle_type}\n"
                f"📏 Distance: {self.estimated_distance} km\n"
                f"💰 Fare: ₹{self.estimated_fare}\n"
                f"💳 Payment: {payment_type.title()}\n\n"
                f"A driver will be assigned shortly!"
            )
            self.clear_fields()

        except sqlite3.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
        except ValueError as err:
            messagebox.showerror("Error", f"Date format error: {err}")
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        """Clear all input fields"""
        self.from_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.payment_type_var.set("cash")
        self.vehicle_type_var.set("Sedan")
        self.estimated_fare = 0
        self.estimated_distance = 0
        self.fare_label.config(
            text="📍 Enter locations and click 'Calculate Fare'",
            fg="#666666"
        )

    def back_to_dashboard(self):
        """Close window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookingPage(root, 1)
    root.mainloop()