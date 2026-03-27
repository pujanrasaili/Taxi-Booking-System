import re
from datetime import datetime, date


class ValidationUtils:
    """Centralized validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        Returns: (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "Email is required"
        
        email = email.strip()
        
        # Basic format check
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        
        # Advanced email pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format. Example: user@example.com"
        
        # Check for common mistakes
        if email.count("@") > 1:
            return False, "Email cannot contain multiple @ symbols"
        
        local_part, domain = email.split("@")
        if len(local_part) < 1:
            return False, "Email must have characters before @"
        if len(domain) < 3:
            return False, "Invalid email domain"
        
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """
        Validate password strength
        Returns: (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 50:
            return False, "Password must not exceed 50 characters"
        
        # Check for at least one letter
        if not any(c.isalpha() for c in password):
            return False, "Password must contain at least one letter"
        
        # Check for at least one number
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        return True, ""
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number
        Returns: (is_valid, error_message)
        """
        if not phone or not phone.strip():
            return False, "Phone number is required"
        
        phone = phone.strip()
        
       # Remove common separators
        phone_clean = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")

        # Remove country code +977
        if phone_clean.startswith("+977"):
            phone_clean = phone_clean[4:]

        # Remove leading 01 (area code)
        if phone_clean.startswith("01"):
            phone_clean = phone_clean[2:]
        
        # Must be exactly 10 digits
        if len(phone_clean) != 10:
            return False, "Phone number must be 10 digits"
        
        # Must be all digits
        if not phone_clean.isdigit():
            return False, "Phone number must contain only digits"
        
        # Indian mobile numbers start with 6, 7, 8, or 9
        if phone_clean[0] not in ['6', '7', '8', '9']:
            return False, "Invalid phone number. Must start with 6, 7, 8, or 9"
        
        return True, ""
    
    @staticmethod
    def validate_name(name, field_name="Name"):
        """
        Validate name (no numbers or special characters)
        Returns: (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, f"{field_name} is required"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters long"
        
        if len(name) > 100:
            return False, f"{field_name} must not exceed 100 characters"
        
        # Allow letters, spaces, dots, and hyphens only
        if not re.match(r'^[a-zA-Z\s.\-]+$', name):
            return False, f"{field_name} can only contain letters, spaces, dots, and hyphens"
        
        # Check for excessive spaces
        if "  " in name:
            return False, f"{field_name} cannot contain multiple consecutive spaces"
        
        return True, ""
    
    @staticmethod
    def validate_license_number(license_num):
        """
        Validate driver's license number
        Returns: (is_valid, error_message)
        """
        if not license_num or not license_num.strip():
            return False, "License number is required"
        
        license_num = license_num.strip().upper()
        
        if len(license_num) < 5:
            return False, "License number must be at least 5 characters"
        
        if len(license_num) > 20:
            return False, "License number must not exceed 20 characters"
        
        # Allow alphanumeric characters only
        if not re.match(r'^[A-Z0-9]+$', license_num):
            return False, "License number can only contain letters and numbers"
        
        return True, ""
    
    @staticmethod
    def validate_vehicle_number(vehicle_num):
        """
        Validate vehicle number (Indian format: KA01AB1234)
        Returns: (is_valid, error_message)
        """
        if not vehicle_num or not vehicle_num.strip():
            return False, "Vehicle number is required"
        
        vehicle_num = vehicle_num.strip().upper().replace(" ", "").replace("-", "")
        
        # format: 2 letters + 2 digits + 1-2 letters + 1-4 digits
        # Examples: KA01AB1234, MH12DE3456
        pattern = r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{1,4}$'
        
        if not re.match(pattern, vehicle_num):
            return False, "Invalid vehicle number format. Example: KA01AB1234"
        
        return True, ""
    
    @staticmethod
    def validate_booking_date(booking_date_str):
        """
        Validate booking date (must be today or future)
        Returns: (is_valid, error_message)
        """
        if not booking_date_str or not booking_date_str.strip():
            return False, "Booking date is required"
        
        try:
            # Try multiple date formats
            booking_date = None
            formats = ["%Y-%m-%d", "%m/%d/%y", "%d/%m/%Y"]
            
            for fmt in formats:
                try:
                    booking_date = datetime.strptime(booking_date_str, fmt).date()
                    break
                except ValueError:
                    continue
            
            if booking_date is None:
                return False, "Invalid date format. Use YYYY-MM-DD"
            
            # Check if date is in the past
            today = date.today()
            if booking_date < today:
                return False, "Cannot book for past dates. Please select today or a future date"
            
            # Check if date is too far in future (e.g., more than 90 days)
            days_ahead = (booking_date - today).days
            if days_ahead > 90:
                return False, "Cannot book more than 90 days in advance"
            
            return True, ""
            
        except Exception as e:
            return False, f"Invalid date: {str(e)}"
    
    @staticmethod
    def validate_booking_time(booking_date_str, booking_time_str):
        """
        Validate booking time (must not be in the past for today's bookings)
        Returns: (is_valid, error_message)
        """
        if not booking_time_str or not booking_time_str.strip():
            return False, "Booking time is required"
        
        try:
            # Parse date
            booking_date = None
            formats = ["%Y-%m-%d", "%m/%d/%y", "%d/%m/%Y"]
            
            for fmt in formats:
                try:
                    booking_date = datetime.strptime(booking_date_str, fmt).date()
                    break
                except ValueError:
                    continue
            
            if booking_date is None:
                return False, "Invalid date format"
            
            # Parse time
            time_str = booking_time_str.strip()
            if ":" not in time_str:
                return False, "Invalid time format. Use HH:MM"
            
            try:
                hour, minute = time_str.split(":")
                hour = int(hour)
                minute = int(minute)
            except:
                return False, "Invalid time format. Use HH:MM"
            
            if hour < 0 or hour > 23:
                return False, "Hour must be between 0 and 23"
            
            if minute < 0 or minute > 59:
                return False, "Minute must be between 0 and 59"
            
            # If booking for today, check if time is in future
            today = date.today()
            if booking_date == today:
                now = datetime.now()
                booking_datetime = datetime.combine(booking_date, datetime.strptime(time_str, "%H:%M").time())
                
                if booking_datetime <= now:
                    return False, "Cannot book for past time. Please select a future time"
                
                # Require at least 30 minutes advance booking
                time_diff = (booking_datetime - now).total_seconds() / 60
                if time_diff < 30:
                    return False, "Please book at least 30 minutes in advance"
            
            return True, ""
            
        except Exception as e:
            return False, f"Invalid time: {str(e)}"
    
    @staticmethod
    def validate_location(location, field_name="Location"):
        """
        Validate location (pickup/dropoff)
        Returns: (is_valid, error_message)
        """
        if not location or not location.strip():
            return False, f"{field_name} is required"
        
        location = location.strip()
        
        if len(location) < 3:
            return False, f"{field_name} must be at least 3 characters"
        
        if len(location) > 200:
            return False, f"{field_name} must not exceed 200 characters"
        
        # Basic validation - allow letters, numbers, spaces, and common punctuation
        if not re.match(r'^[a-zA-Z0-9\s,.\-/#]+$', location):
            return False, f"{field_name} contains invalid characters"
        
        return True, ""
    
    @staticmethod
    def validate_same_location(pickup, dropoff):
        """
        Check if pickup and dropoff are the same
        Returns: (is_valid, error_message)
        """
        if not pickup or not dropoff:
            return True, ""  # Other validations will catch empty fields
        
        pickup_clean = pickup.strip().lower()
        dropoff_clean = dropoff.strip().lower()
        
        if pickup_clean == dropoff_clean:
            return False, "Pickup and dropoff locations cannot be the same"
        
        return True, ""
    
    @staticmethod
    def validate_address(address):
        """
        Validate address
        Returns: (is_valid, error_message)
        """
        if not address or not address.strip():
            return False, "Address is required"
        
        address = address.strip()
        
        if len(address) < 3:
            return False, "Address must be at least 3 characters (provide full address)"
        
        if len(address) > 500:
            return False, "Address must not exceed 500 characters"
        
        return True, ""
    
    @staticmethod
    def validate_fare(fare):
        """
        Validate fare amount
        Returns: (is_valid, error_message)
        """
        try:
            fare_amount = float(fare)
            
            if fare_amount <= 0:
                return False, "Fare must be greater than 0"
            
            if fare_amount < 10:
                return False, "Fare cannot be less than ₹10"
            
            if fare_amount > 10000:
                return False, "Fare cannot exceed ₹10,000. Please contact admin for long-distance bookings"
            
            return True, ""
            
        except (ValueError, TypeError):
            return False, "Invalid fare amount"
    
    @staticmethod
    def validate_distance(distance):
        """
        Validate distance
        Returns: (is_valid, error_message)
        """
        try:
            dist = float(distance)
            
            if dist <= 0:
                return False, "Distance must be greater than 0"
            
            if dist < 1:
                return False, "Distance must be at least 1 km"
            
            if dist > 500:
                return False, "Distance cannot exceed 500 km. Please contact admin for long-distance bookings"
            
            return True, ""
            
        except (ValueError, TypeError):
            return False, "Invalid distance"