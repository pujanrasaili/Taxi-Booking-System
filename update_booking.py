import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from config import DB_PATH
from validation_utils import ValidationUtils  # NEW IMPORT


class UpdateBookingPage:
    """Update booking feature with ALL VALIDATIONS"""

    def __init__(self, root, customer_id):
        self.root = root
        self.customer_id = customer_id
        self.root.title("Update Booking")
        self.root.geometry("600x900")
        self.root.configure(bg="#000000")
        
        self.selected_booking_id = None

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#DDC01A", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_label = tk.Label(
            header_frame,
            text="Update Your Booking",
            bg="#DDC01A",
            fg="white",
            font=("Helvetica", 16, "bold")
        )
        header_label.pack(expand=True)

        # Main container with scrolling
        container = tk.Frame(self.root, bg="#000000")
        container.pack(fill="both", expand=True)

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

        # Step 1: Select Booking
        tk.Label(
            main_frame, 
            text="Step 1: Select Booking to Update", 
            bg="#ffffff", 
            font=("Helvetica", 14, "bold"),
            fg="#007bff"
        ).pack(pady=10)

        tk.Label(main_frame, text="Select Your Booking:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        
        self.booking_var = tk.StringVar()
        self.booking_dropdown = ttk.Combobox(
            main_frame,
            textvariable=self.booking_var,
            font=("Helvetica", 11),
            state="readonly",
            width=50
        )
        self.booking_dropdown.pack(pady=5)
        self.booking_dropdown.bind('<<ComboboxSelected>>', self.load_booking_details)
        
        load_btn = tk.Button(
            main_frame,
            text="📂 Load Booking Details",
            bg="#17a2b8",
            fg="white",
            font=("Helvetica", 12),
            width=25,
            relief="flat",
            command=self.load_booking_details
        )
        load_btn.pack(pady=10)

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        # Step 2: Update Fields
        tk.Label(
            main_frame, 
            text="Step 2: Update Booking Information", 
            bg="#ffffff", 
            font=("Helvetica", 14, "bold"),
            fg="#28a745"
        ).pack(pady=10)

        # Pickup Location
        tk.Label(main_frame, text="Pickup Location:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.pickup_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.pickup_entry.pack(pady=5)

        # Dropoff Location
        tk.Label(main_frame, text="Drop-off Location:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.dropoff_entry = tk.Entry(main_frame, font=("Helvetica", 12), bd=2, relief="solid", width=40)
        self.dropoff_entry.pack(pady=5)

        # Vehicle Type
        tk.Label(main_frame, text="Vehicle Type:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.vehicle_var = tk.StringVar(value="Sedan")
        
        vehicle_frame = tk.Frame(main_frame, bg="#ffffff")
        vehicle_frame.pack(pady=5, fill="x")
        
        vehicles = ["Sedan", "SUV", "Hatchback", "Van", "Bike"]
        for vehicle in vehicles:
            rb = tk.Radiobutton(
                vehicle_frame,
                text=vehicle,
                variable=self.vehicle_var,
                value=vehicle,
                bg="#ffffff",
                font=("Helvetica", 10)
            )
            rb.pack(side="left", padx=5)

        # Date Selection
        tk.Label(main_frame, text="Booking Date:", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        self.calendar = Calendar(main_frame, font=("Helvetica", 11), selectmode='day')
        self.calendar.pack(pady=5)

        # Time Selection
        tk.Label(main_frame, text="Pickup Time (HH:MM):", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        time_frame = tk.Frame(main_frame, bg="#ffffff")
        time_frame.pack(pady=5)

        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")

        hours = [f"{h:02}" for h in range(24)]
        minutes = [f"{m:02}" for m in range(0, 60, 5)]

        tk.Label(time_frame, text="Hour:", bg="#ffffff", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        hour_dropdown = tk.OptionMenu(time_frame, self.hour_var, *hours)
        hour_dropdown.grid(row=0, column=1, padx=5)

        tk.Label(time_frame, text="Minute:", bg="#ffffff", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)
        minute_dropdown = tk.OptionMenu(time_frame, self.minute_var, *minutes)
        minute_dropdown.grid(row=0, column=3, padx=5)

        # Status Info
        self.status_label = tk.Label(
            main_frame,
            text="Select a booking to update",
            bg="#f0f0f0",
            font=("Helvetica", 11),
            fg="#666666",
            pady=10,
            bd=2,
            relief="groove"
        )
        self.status_label.pack(fill="x", pady=10)

        # Update Button
        update_btn = tk.Button(
            main_frame,
            text="✓ Update Booking",
            bg="#28a745",
            fg="white",
            font=("Helvetica", 14, "bold"),
            width=25,
            relief="flat",
            command=self.update_booking
        )
        update_btn.pack(pady=15)

        # Back Button
        back_btn = tk.Button(
            main_frame,
            text="← Back to Dashboard",
            bg="#000000",
            fg="white",
            font=("Helvetica", 12),
            width=25,
            relief="flat",
            command=self.back_to_dashboard
        )
        back_btn.pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.load_updateable_bookings()

    def load_updateable_bookings(self):
        """Load bookings that can be updated"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            query = """
                SELECT booking_id, pickup_location, dropoff_location, 
                       booking_date, pickup_time, status, vehicle_type
                FROM bookings
                WHERE customer_id = ? AND status IN ('pending', 'in_progress', 'accepted')
                ORDER BY booking_date DESC
            """
            cursor.execute(query, (self.customer_id,))
            bookings = cursor.fetchall()
            
            if bookings:
                booking_list = [
                    f"ID:{b[0]} | {b[1]} → {b[2]} | {b[3]} {b[4]} | {b[5]} | {b[6]}"
                    for b in bookings
                ]
                self.booking_dropdown['values'] = booking_list
                self.status_label.config(
                    text=f"✅ {len(bookings)} booking(s) available for update",
                    fg="#28a745",
                    bg="#d4edda"
                )
            else:
                self.booking_dropdown['values'] = []
                self.status_label.config(
                    text="⚠️ No bookings available for update. Only pending/in-progress bookings can be updated.",
                    fg="#856404",
                    bg="#fff3cd"
                )
                
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error loading bookings: {err}")
        finally:
            if conn:
                conn.close()

    def load_booking_details(self, event=None):
        """Load selected booking details"""
        selection = self.booking_var.get()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a booking first!")
            return
        
        booking_id = selection.split("|")[0].replace("ID:", "").strip()
        self.selected_booking_id = booking_id
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT pickup_location, dropoff_location, booking_date, 
                       pickup_time, vehicle_type, status
                FROM bookings
                WHERE booking_id = ?
            """, (booking_id,))
            
            result = cursor.fetchone()
            
            if result:
                self.pickup_entry.delete(0, tk.END)
                self.pickup_entry.insert(0, result[0])
                
                self.dropoff_entry.delete(0, tk.END)
                self.dropoff_entry.insert(0, result[1])
                
                date_obj = datetime.strptime(result[2], "%Y-%m-%d")
                self.calendar.selection_set(date_obj)
                
                time_str = result[3].split()[1] if len(result[3].split()) > 1 else "12:00:00"
                hour, minute = time_str.split(":")[:2]
                self.hour_var.set(hour)
                self.minute_var.set(minute)
                
                self.vehicle_var.set(result[4])
                
                self.status_label.config(
                    text=f"📋 Booking #{booking_id} loaded | Status: {result[5]} | Ready to update!",
                    fg="#004085",
                    bg="#cce5ff"
                )
                
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error loading booking: {err}")
        finally:
            if conn:
                conn.close()

    def update_booking(self):
        """Update booking with ALL VALIDATIONS"""
        if not self.selected_booking_id:
            messagebox.showerror("Error", "Please select and load a booking first!")
            return
        
        pickup = self.pickup_entry.get().strip()
        dropoff = self.dropoff_entry.get().strip()
        vehicle = self.vehicle_var.get()
        date = self.calendar.get_date()
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"
        
        # ✅ VALIDATION 1: Check locations
        is_valid, error_msg = ValidationUtils.validate_location(pickup, "Pickup location")
        if not is_valid:
            messagebox.showerror("Invalid Pickup", error_msg)
            self.pickup_entry.focus()
            return
        
        is_valid, error_msg = ValidationUtils.validate_location(dropoff, "Drop-off location")
        if not is_valid:
            messagebox.showerror("Invalid Dropoff", error_msg)
            self.dropoff_entry.focus()
            return
        
        # ✅ VALIDATION 2: Same location check
        is_valid, error_msg = ValidationUtils.validate_same_location(pickup, dropoff)
        if not is_valid:
            messagebox.showerror("Same Location", error_msg)
            return
        
        try:
            date_obj = datetime.strptime(date, "%m/%d/%y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            
            # ✅ VALIDATION 3: Date validation
            is_valid, error_msg = ValidationUtils.validate_booking_date(formatted_date)
            if not is_valid:
                messagebox.showerror("Invalid Date", error_msg)
                return
            
            # ✅ VALIDATION 4: Time validation
            is_valid, error_msg = ValidationUtils.validate_booking_time(formatted_date, time)
            if not is_valid:
                messagebox.showerror("Invalid Time", error_msg)
                return
            
            pickup_datetime = f"{formatted_date} {time}:00"
            
            # Confirm update
            confirm = messagebox.askyesno(
                "Confirm Update",
                f"Update Booking #{self.selected_booking_id}?\n\n"
                f"📍 From: {pickup}\n"
                f"📍 To: {dropoff}\n"
                f"📅 Date: {formatted_date}\n"
                f"🕐 Time: {time}\n"
                f"🚗 Vehicle: {vehicle}\n\n"
                f"✅ All validations passed!"
            )
            
            if not confirm:
                return
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # ✅ VALIDATION 5: Check status
            cursor.execute("SELECT status FROM bookings WHERE booking_id = ?", (self.selected_booking_id,))
            result = cursor.fetchone()
            
            if result and result[0] in ['started', 'completed', 'cancelled']:
                messagebox.showerror(
                    "Cannot Update",
                    f"Cannot update booking with status: {result[0]}\n\n"
                    "Only pending, in_progress, or accepted bookings can be updated."
                )
                return
            
            # Update booking
            query = """
                UPDATE bookings 
                SET pickup_location = ?, dropoff_location = ?, 
                    booking_date = ?, pickup_time = ?, vehicle_type = ?
                WHERE booking_id = ?
            """
            cursor.execute(query, (
                pickup, dropoff, formatted_date, 
                pickup_datetime, vehicle, self.selected_booking_id
            ))
            
            conn.commit()
            
            messagebox.showinfo(
                "✅ Update Successful!",
                f"Booking #{self.selected_booking_id} updated successfully!\n\n"
                f"📍 From: {pickup}\n"
                f"📍 To: {dropoff}\n"
                f"📅 Date: {formatted_date}\n"
                f"🕐 Time: {time}\n"
                f"🚗 Vehicle: {vehicle}\n\n"
                f"All changes have been saved!"
            )
            
            self.load_updateable_bookings()
            self.selected_booking_id = None
            self.status_label.config(
                text="Select another booking to update",
                fg="#666666",
                bg="#f0f0f0"
            )
            
        except ValueError as err:
            messagebox.showerror("Error", f"Date format error: {err}")
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error updating booking: {err}")
        finally:
            if conn:
                conn.close()

    def back_to_dashboard(self):
        """Close window"""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateBookingPage(root, 1)
    root.mainloop()