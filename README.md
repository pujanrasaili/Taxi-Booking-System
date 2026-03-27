# 🚖 Taxi Booking System

A desktop taxi booking application built with Python, Tkinter, and SQLite — supporting customers, drivers, and admins with a full booking management workflow.

## 📸 Features

### 👤 Customer
- Register and login
- Book a ride (choose vehicle type, pickup/dropoff, date & time)
- View, update, and cancel bookings
- Fare estimate with peak hour & night surcharge

### 🚗 Driver
- Self-registration (pending admin approval)
- View and accept assigned bookings
- Update trip status (accepted → started → completed)

### 🛠️ Admin
- Approve or reject driver registrations
- Manage all bookings
- View all customers and drivers

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3 | Core language |
| Tkinter | GUI framework |
| SQLite | Local database |

## 🚀 How to Run

1. Clone or download this repository
2. Make sure Python 3 is installed
3. Install Pillow (for images):
```
   pip install pillow
```
4. Set up the database:
```
   python database_setup.py
```
5. Launch the app:
```
   python start.py
```

## 🔑 Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Customer | customer@gmail.com | customer123 |
| Driver | ram@gmail.com | ram123 |
| Admin | admin@gmail.com | admin123 |

## 💰 Fare Calculation

| Vehicle | Base Fare | Per KM |
|---------|-----------|--------|
| Bike | Rs. 30 | Rs. 8 |
| Hatchback | Rs. 40 | Rs. 10 |
| Sedan | Rs. 50 | Rs. 12 |
| SUV | Rs. 80 | Rs. 18 |
| Van | Rs. 100 | Rs. 20 |

> Peak hours (8–10 AM, 5–8 PM): 1.5x multiplier  
> Night hours (11 PM–6 AM): 1.3x multiplier

## 📁 Project Structure
```
├── start.py              # App entry point
├── login.py              # Login page
├── register.py           # Customer registration
├── customer_dashboard.py # Customer main screen
├── driver_dashboard.py   # Driver main screen
├── admin_dashboard.py    # Admin main screen
├── booking.py            # Book a ride
├── fare_calculator.py    # Fare logic
├── database_setup.py     # DB initialisation
├── config.py             # App configuration
└── validation_utils.py   # Input validation
```

## 👨‍💻 Author

**Pujan Rasaili**
