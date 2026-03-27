import sqlite3
from config import DB_PATH


def create_database():
    """Create SQLite database with all required fields"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Customers table WITH ADDRESS (missing in your code)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add address column if it doesn't exist (for existing databases)
    cursor.execute("PRAGMA table_info(customers)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'address' not in columns:
        cursor.execute("ALTER TABLE customers ADD COLUMN address TEXT DEFAULT 'Not specified'")
        print("✅ Added 'address' column to customers table")
    
    # Create Drivers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            license_number TEXT NOT NULL UNIQUE,
            vehicle_number TEXT NOT NULL UNIQUE,
            vehicle_type TEXT NOT NULL,
            status TEXT DEFAULT 'offline',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Admin table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            aid INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            contact_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            driver_id INTEGER,
            pickup_location TEXT NOT NULL,
            dropoff_location TEXT NOT NULL,
            pickup_time DATETIME NOT NULL,
            booking_date DATE NOT NULL,
            status TEXT DEFAULT 'pending',
            fare REAL DEFAULT 0.0,
            distance REAL DEFAULT 0.0,
            vehicle_type TEXT DEFAULT 'Sedan',
            payment_type TEXT DEFAULT 'cash',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
        )
    """)
    
    # Check and add missing columns
    cursor.execute("PRAGMA table_info(bookings)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'fare' not in columns:
        cursor.execute("ALTER TABLE bookings ADD COLUMN fare REAL DEFAULT 0.0")
        print("✅ Added 'fare' column to bookings table")
    
    if 'distance' not in columns:
        cursor.execute("ALTER TABLE bookings ADD COLUMN distance REAL DEFAULT 0.0")
        print("✅ Added 'distance' column to bookings table")
    
    if 'vehicle_type' not in columns:
        cursor.execute("ALTER TABLE bookings ADD COLUMN vehicle_type TEXT DEFAULT 'Sedan'")
        print("✅ Added 'vehicle_type' column to bookings table")
    
    # Insert default admin
    cursor.execute("""
        INSERT OR IGNORE INTO admin (full_name, email, password, contact_number)
        VALUES ('System Admin', 'admin@gmail.com', 'admin123', '9876543210')
    """)
    
    # Insert sample drivers
    sample_drivers = [
        ('Ram Driver', 'ram@gmail.com', '9876543211', 'ram123', 'DL12345', 'KA01AB1234', 'Sedan', 'available'),
        ('Shyam Driver', 'shyam@gmail.com', '9876543212', 'shyam123', 'DL12346', 'KA01AB1235', 'SUV', 'available'),
        ('Sita Driver', 'sita@gmail.com', '9876543213', 'sita123', 'DL12347', 'KA01AB1236', 'Hatchback', 'available'),
        ('Gita Driver', 'gita@gmail.com', '9876543214', 'gita123', 'DL12348', 'KA01AB1237', 'Van', 'available'),
        ('Hari Driver', 'hari@gmail.com', '9876543215', 'hari123', 'DL12349', 'KA01AB1238', 'Bike', 'available')
    ]
    
    for driver in sample_drivers:
        try:
            cursor.execute("""
                INSERT INTO drivers 
                (name, email, phone, password, license_number, vehicle_number, vehicle_type, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, driver)
        except sqlite3.IntegrityError:
            pass
    
    # Insert sample customer WITH ADDRESS
    try:
        cursor.execute("""
            INSERT INTO customers (name, address, email, password, phone)
            VALUES ('Test Customer', '123 Main Street, City', 'customer@gmail.com', 'customer123', '9876543220')
        """)
    except sqlite3.IntegrityError:
        pass
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database created/updated successfully!")
    print(f"📁 Database location: {DB_PATH}")
    print("\n🔑 Test Accounts:")
    print("Customer: customer@gmail.com / customer123")
    print("Driver: ram@gmail.com / ram123")
    print("Admin: admin@gmail.com / admin123")
    print("\n⚠️  IMPORTANT: Address field has been added to customers table!")


if __name__ == "__main__":
    create_database()