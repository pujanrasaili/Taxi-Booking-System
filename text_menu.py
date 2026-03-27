"""
Text-Based Menu System for Taxi Booking
Add this file: text_menu.py
Run this instead of start.py to meet assignment requirements
"""

import sqlite3
from datetime import datetime
from config import DB_PATH


class TextBasedTaxiSystem:
    """Text-based menu system as required by assignment"""
    
    def __init__(self):
        self.current_user = None
        self.user_type = None
        
    def main_menu(self):
        """Main menu for the system"""
        while True:
            print("\n" + "="*50)
            print("  TAXI BOOKING SYSTEM - TEXT MENU")
            print("="*50)
            print("1. Customer Login")
            print("2. Customer Registration")
            print("3. Driver Login")
            print("4. Administrator Login")
            print("5. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.customer_login()
            elif choice == '2':
                self.customer_registration()
            elif choice == '3':
                self.driver_login()
            elif choice == '4':
                self.admin_login()
            elif choice == '5':
                print("\n✅ Thank you for using Taxi Booking System!")
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def customer_registration(self):
        """Customer registration"""
        print("\n" + "="*50)
        print("  CUSTOMER REGISTRATION")
        print("="*50)
        
        name = input("Enter your name: ").strip()
        address = input("Enter your address: ").strip()  # MISSING IN YOUR CODE
        phone = input("Enter phone number (10 digits): ").strip()
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        
        # Validation
        if not all([name, address, phone, email, password]):
            print("❌ All fields are required!")
            return
        
        if len(phone) != 10 or not phone.isdigit():
            print("❌ Phone number must be 10 digits!")
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT COUNT(*) FROM customers WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                print("❌ Email already exists!")
                return
            
            # Insert customer (need to add address column)
            cursor.execute("""
                INSERT INTO customers (name, address, phone, email, password)
                VALUES (?, ?, ?, ?, ?)
            """, (name, address, phone, email, password))
            
            conn.commit()
            print(f"\n✅ Registration successful! Welcome {name}!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def customer_login(self):
        """Customer login"""
        print("\n" + "="*50)
        print("  CUSTOMER LOGIN")
        print("="*50)
        
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT customer_id, name FROM customers 
                WHERE email = ? AND password = ?
            """, (email, password))
            
            result = cursor.fetchone()
            
            if result:
                self.current_user = result[0]
                self.user_type = 'customer'
                print(f"\n✅ Login successful! Welcome {result[1]}!")
                self.customer_menu()
            else:
                print("❌ Invalid email or password!")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def customer_menu(self):
        """Customer menu"""
        while True:
            print("\n" + "="*50)
            print("  CUSTOMER MENU")
            print("="*50)
            print("1. Book a Taxi")
            print("2. View My Bookings")
            print("3. Update Booking")  # MISSING IN YOUR CODE
            print("4. Cancel Booking")
            print("5. Logout")
            print("="*50)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.book_taxi()
            elif choice == '2':
                self.view_bookings()
            elif choice == '3':
                self.update_booking()  # NEW FUNCTION NEEDED
            elif choice == '4':
                self.cancel_booking()
            elif choice == '5':
                print("✅ Logged out successfully!")
                self.current_user = None
                self.user_type = None
                break
            else:
                print("❌ Invalid choice!")
    
    def book_taxi(self):
        """Book a taxi"""
        print("\n" + "="*50)
        print("  BOOK A TAXI")
        print("="*50)
        
        pickup = input("Enter pickup location: ").strip()
        dropoff = input("Enter drop-off location: ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()
        time = input("Enter time (HH:MM): ").strip()
        vehicle = input("Vehicle type (Sedan/SUV/Hatchback/Van/Bike): ").strip()
        
        if not all([pickup, dropoff, date, time, vehicle]):
            print("❌ All fields are required!")
            return
        
        try:
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            pickup_datetime = f"{date} {time}:00"
            
            cursor.execute("""
                INSERT INTO bookings 
                (customer_id, pickup_location, dropoff_location, pickup_time, 
                 booking_date, vehicle_type, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """, (self.current_user, pickup, dropoff, pickup_datetime, date, vehicle))
            
            conn.commit()
            print("\n✅ Booking created successfully!")
            print(f"Booking ID: {cursor.lastrowid}")
            
        except ValueError:
            print("❌ Invalid date/time format!")
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def view_bookings(self):
        """View customer bookings"""
        print("\n" + "="*50)
        print("  MY BOOKINGS")
        print("="*50)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT b.booking_id, b.pickup_location, b.dropoff_location,
                       b.booking_date, b.pickup_time, b.status,
                       COALESCE(d.name, 'Not Assigned') as driver_name
                FROM bookings b
                LEFT JOIN drivers d ON b.driver_id = d.driver_id
                WHERE b.customer_id = ?
                ORDER BY b.booking_date DESC
            """, (self.current_user,))
            
            bookings = cursor.fetchall()
            
            if not bookings:
                print("📋 No bookings found.")
                return
            
            for booking in bookings:
                print(f"\nBooking ID: {booking[0]}")
                print(f"From: {booking[1]}")
                print(f"To: {booking[2]}")
                print(f"Date: {booking[3]}")
                print(f"Time: {booking[4]}")
                print(f"Status: {booking[5]}")
                print(f"Driver: {booking[6]}")
                print("-" * 50)
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def update_booking(self):
        """Update booking - MISSING IN YOUR CODE"""
        print("\n" + "="*50)
        print("  UPDATE BOOKING")
        print("="*50)
        
        booking_id = input("Enter booking ID to update: ").strip()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Check if booking exists and belongs to customer
            cursor.execute("""
                SELECT status FROM bookings 
                WHERE booking_id = ? AND customer_id = ?
            """, (booking_id, self.current_user))
            
            result = cursor.fetchone()
            
            if not result:
                print("❌ Booking not found!")
                return
            
            if result[0] not in ['pending', 'in_progress']:
                print("❌ Cannot update booking with status:", result[0])
                return
            
            print("\nWhat would you like to update?")
            print("1. Pickup location")
            print("2. Drop-off location")
            print("3. Date and time")
            print("4. Cancel")
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == '1':
                new_pickup = input("Enter new pickup location: ").strip()
                cursor.execute("""
                    UPDATE bookings SET pickup_location = ?
                    WHERE booking_id = ?
                """, (new_pickup, booking_id))
                print("✅ Pickup location updated!")
                
            elif choice == '2':
                new_dropoff = input("Enter new drop-off location: ").strip()
                cursor.execute("""
                    UPDATE bookings SET dropoff_location = ?
                    WHERE booking_id = ?
                """, (new_dropoff, booking_id))
                print("✅ Drop-off location updated!")
                
            elif choice == '3':
                new_date = input("Enter new date (YYYY-MM-DD): ").strip()
                new_time = input("Enter new time (HH:MM): ").strip()
                new_datetime = f"{new_date} {new_time}:00"
                
                cursor.execute("""
                    UPDATE bookings SET booking_date = ?, pickup_time = ?
                    WHERE booking_id = ?
                """, (new_date, new_datetime, booking_id))
                print("✅ Date and time updated!")
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def cancel_booking(self):
        """Cancel booking"""
        print("\n" + "="*50)
        print("  CANCEL BOOKING")
        print("="*50)
        
        booking_id = input("Enter booking ID to cancel: ").strip()
        
        confirm = input(f"Are you sure you want to cancel booking {booking_id}? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Cancellation aborted.")
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE bookings SET status = 'cancelled'
                WHERE booking_id = ? AND customer_id = ?
            """, (booking_id, self.current_user))
            
            if cursor.rowcount > 0:
                conn.commit()
                print("✅ Booking cancelled successfully!")
            else:
                print("❌ Booking not found!")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def driver_login(self):
        """Driver login"""
        print("\n" + "="*50)
        print("  DRIVER LOGIN")
        print("="*50)
        
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT driver_id, name FROM drivers 
                WHERE email = ? AND password = ?
            """, (email, password))
            
            result = cursor.fetchone()
            
            if result:
                self.current_user = result[0]
                self.user_type = 'driver'
                print(f"\n✅ Login successful! Welcome {result[1]}!")
                self.driver_menu()
            else:
                print("❌ Invalid email or password!")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def driver_menu(self):
        """Driver menu"""
        while True:
            print("\n" + "="*50)
            print("  DRIVER MENU")
            print("="*50)
            print("1. View My Assigned Trips")
            print("2. Logout")
            print("="*50)
            
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == '1':
                self.view_driver_trips()
            elif choice == '2':
                print("✅ Logged out successfully!")
                self.current_user = None
                self.user_type = None
                break
            else:
                print("❌ Invalid choice!")
    
    def view_driver_trips(self):
        """View driver's assigned trips"""
        print("\n" + "="*50)
        print("  MY ASSIGNED TRIPS")
        print("="*50)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location,
                       b.booking_date, b.pickup_time, b.status
                FROM bookings b
                JOIN customers c ON b.customer_id = c.customer_id
                WHERE b.driver_id = ?
                ORDER BY b.booking_date, b.pickup_time
            """, (self.current_user,))
            
            trips = cursor.fetchall()
            
            if not trips:
                print("📋 No trips assigned yet.")
                return
            
            for trip in trips:
                print(f"\nBooking ID: {trip[0]}")
                print(f"Customer: {trip[1]}")
                print(f"From: {trip[2]}")
                print(f"To: {trip[3]}")
                print(f"Date: {trip[4]}")
                print(f"Time: {trip[5]}")
                print(f"Status: {trip[6]}")
                print("-" * 50)
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def admin_login(self):
        """Admin login"""
        print("\n" + "="*50)
        print("  ADMINISTRATOR LOGIN")
        print("="*50)
        
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT aid, full_name FROM admin 
                WHERE email = ? AND password = ?
            """, (email, password))
            
            result = cursor.fetchone()
            
            if result:
                self.current_user = result[0]
                self.user_type = 'admin'
                print(f"\n✅ Login successful! Welcome {result[1]}!")
                self.admin_menu()
            else:
                print("❌ Invalid email or password!")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def admin_menu(self):
        """Admin menu"""
        while True:
            print("\n" + "="*50)
            print("  ADMINISTRATOR MENU")
            print("="*50)
            print("1. View All Bookings")
            print("2. Assign Driver to Booking")
            print("3. Logout")
            print("="*50)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.view_all_bookings()
            elif choice == '2':
                self.assign_driver_to_booking()
            elif choice == '3':
                print("✅ Logged out successfully!")
                self.current_user = None
                self.user_type = None
                break
            else:
                print("❌ Invalid choice!")
    
    def view_all_bookings(self):
        """View all bookings"""
        print("\n" + "="*50)
        print("  ALL BOOKINGS")
        print("="*50)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location,
                       b.booking_date, b.pickup_time, b.status,
                       COALESCE(d.name, 'Not Assigned') as driver_name
                FROM bookings b
                JOIN customers c ON b.customer_id = c.customer_id
                LEFT JOIN drivers d ON b.driver_id = d.driver_id
                ORDER BY b.booking_date DESC, b.pickup_time DESC
            """)
            
            bookings = cursor.fetchall()
            
            if not bookings:
                print("📋 No bookings found.")
                return
            
            for booking in bookings:
                print(f"\nBooking ID: {booking[0]}")
                print(f"Customer: {booking[1]}")
                print(f"From: {booking[2]}")
                print(f"To: {booking[3]}")
                print(f"Date: {booking[4]}")
                print(f"Time: {booking[5]}")
                print(f"Status: {booking[6]}")
                print(f"Driver: {booking[7]}")
                print("-" * 50)
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def assign_driver_to_booking(self):
        """Assign driver with overlap check - MISSING IN YOUR CODE"""
        print("\n" + "="*50)
        print("  ASSIGN DRIVER TO BOOKING")
        print("="*50)
        
        booking_id = input("Enter booking ID: ").strip()
        driver_id = input("Enter driver ID: ").strip()
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Get booking details
            cursor.execute("""
                SELECT pickup_time, booking_date FROM bookings
                WHERE booking_id = ?
            """, (booking_id,))
            
            booking_result = cursor.fetchone()
            
            if not booking_result:
                print("❌ Booking not found!")
                return
            
            booking_time = booking_result[0]
            booking_date = booking_result[1]
            
            # CRITICAL: Check for overlapping bookings (MISSING IN YOUR CODE)
            cursor.execute("""
                SELECT COUNT(*) FROM bookings
                WHERE driver_id = ? 
                AND booking_date = ?
                AND status NOT IN ('cancelled', 'completed')
                AND booking_id != ?
            """, (driver_id, booking_date, booking_id))
            
            overlap_count = cursor.fetchone()[0]
            
            if overlap_count > 0:
                print("❌ ERROR: Driver already has a booking on this date!")
                print("⚠️ Assignment requirements: No overlapping bookings allowed!")
                return
            
            # Assign driver
            cursor.execute("""
                UPDATE bookings SET driver_id = ?, status = 'in_progress'
                WHERE booking_id = ?
            """, (driver_id, booking_id))
            
            cursor.execute("""
                UPDATE drivers SET status = 'busy'
                WHERE driver_id = ?
            """, (driver_id,))
            
            conn.commit()
            print("✅ Driver assigned successfully (no overlap detected)!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    print("="*50)
    print("  TAXI BOOKING SYSTEM")
    print("  Text-Based Menu Interface")
    print("="*50)
    
    system = TextBasedTaxiSystem()
    system.main_menu()