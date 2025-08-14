-- Create the database (if not exists) and connect
-- From terminal: sqlite3 cars.db

-- Enable foreign key constraints (important for relationships)
PRAGMA foreign_keys = ON;

-- Create Cars table
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    price REAL NOT NULL CHECK (price > 0),
    mileage INTEGER DEFAULT 0 CHECK (mileage >= 0),
    color TEXT,
    description TEXT,
    image TEXT DEFAULT 'default.jpg',
    available BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_car UNIQUE (make, model, year, mileage)
);

-- Create Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Purchases table
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    purchase_price REAL NOT NULL CHECK (purchase_price > 0),
    payment_method TEXT CHECK (payment_method IN ('Cash', 'Loan', 'Lease', 'Finance')),
    status TEXT DEFAULT 'Completed' CHECK (status IN ('Pending', 'Completed', 'Cancelled')),
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE RESTRICT,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);

-- Create Test Drives table
CREATE TABLE IF NOT EXISTS test_drives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    drive_date TIMESTAMP NOT NULL,
    notes TEXT,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Create Maintenance Records table
CREATE TABLE IF NOT EXISTS maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    service_date TIMESTAMP NOT NULL,
    service_type TEXT NOT NULL,
    cost REAL NOT NULL CHECK (cost >= 0),
    description TEXT,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
);

-- Create triggers for updated_at timestamps
CREATE TRIGGER IF NOT EXISTS update_car_timestamp
AFTER UPDATE ON cars
FOR EACH ROW
BEGIN
    UPDATE cars SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_cars_make_model ON cars(make, model);
CREATE INDEX IF NOT EXISTS idx_cars_price ON cars(price);
CREATE INDEX IF NOT EXISTS idx_purchases_date ON purchases(purchase_date);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
