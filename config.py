"""
Configuration file for Taxi Booking System
Stores database path and system constants
"""

import os

# Database Configuration (SQLite)
DB_PATH = "taxi_booking.db"

# Window Configuration
WINDOW_SIZES = {
    "login": "400x600",
    "dashboard": "800x600",
    "booking": "500x850",
    "admin": "800x600",
    "start": "1000x600"
}

# Color Theme (Yellow, Black, White)
COLORS = {
    "primary": "#DDC01A",
    "secondary": "#000000",
    "background": "#ffffff",
    "text_dark": "#000000",
    "text_light": "#ffffff",
    "success": "#28a745",
    "danger": "#dc3545",
    "info": "#007bff",
    "warning": "#ffc107"
}

# System Constants
PHONE_NUMBER_LENGTH = 10
MIN_PASSWORD_LENGTH = 6

# Fare Configuration
BASE_FARE = {
    "Sedan": 50,
    "SUV": 80,
    "Hatchback": 40,
    "Van": 100,
    "Bike": 30
}

PER_KM_RATE = {
    "Sedan": 12,
    "SUV": 18,
    "Hatchback": 10,
    "Van": 20,
    "Bike": 8
}

# Peak hours: 8-10 AM and 5-8 PM (1.5x multiplier)
PEAK_HOURS = [(8, 10), (17, 20)]
PEAK_HOUR_MULTIPLIER = 1.5

# Night hours: 11 PM - 6 AM (1.3x multiplier)
NIGHT_HOURS = (23, 6)
NIGHT_MULTIPLIER = 1.3

# Driver Status
DRIVER_STATUS = {
    "available": "Available",
    "offline": "Offline",
    "busy": "Busy"
}

# Booking Status
BOOKING_STATUS = {
    "pending": "Pending",
    "in_progress": "In Progress",
    "accepted": "Accepted",
    "started": "Started",
    "completed": "Completed",
    "cancelled": "Cancelled"
}