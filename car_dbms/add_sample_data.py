import sqlite3
from datetime import datetime

def add_sample_data():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    
    # Luxury cars data
    luxury_cars = [
        ('Mercedes-Benz', 'S-Class', 2023, 120000, 1500, 'Obsidian Black', 
         'The pinnacle of luxury with cutting-edge technology and unparalleled comfort.', 
         'mercedes_s_class.jpg', True),
        ('BMW', '7 Series', 2023, 110000, 2000, 'Mineral White', 
         'Executive luxury with sporty DNA and innovative features.', 
         'bmw_7_series.jpg', True),
        ('Audi', 'A8 L', 2023, 105000, 1800, 'Navarra Blue', 
         'Quattro all-wheel drive with premium comfort and virtual cockpit.', 
         'audi_a8.jpg', True),
        ('Porsche', '911 Turbo S', 2023, 215000, 500, 'Guards Red', 
         'Legendary performance meets daily drivability.', 
         'porsche_911.jpg', True),
        ('Bentley', 'Continental GT', 2023, 245000, 1200, 'Beluga Black', 
         'Handcrafted British luxury with W12 power.', 
         'bentley_gt.jpg', True),
        ('Rolls-Royce', 'Ghost', 2023, 350000, 800, 'English White', 
         'The most luxurious way to travel, with whisper-quiet cabin.', 
         'rolls_ghost.jpg', True),
        ('Ferrari', 'Roma', 2023, 250000, 300, 'Rosso Corsa', 
         'Italian elegance with 612 horsepower of pure passion.', 
         'ferrari_roma.jpg', True),
        ('Lamborghini', 'Huracan EVO', 2023, 275000, 400, 'Arancio Borealis', 
         'V10-powered supercar with razor-sharp handling.', 
         'lamborghini_huracan.jpg', True),
        ('Aston Martin', 'DB11', 2023, 220000, 900, 'Skyfall Silver', 
         'James Bond elegance with thunderous V12 performance.', 
         'aston_db11.jpg', True),
        ('Lexus', 'LC 500', 2023, 98000, 2500, 'Structural Blue', 
         'Japanese craftsmanship meets dramatic design.', 
         'lexus_lc.jpg', True)
    ]
    
    # Insert cars
    c.executemany('''INSERT INTO cars 
                    (make, model, year, price, mileage, color, description, image, available)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', luxury_cars)
    
    # Sample purchases
    purchases = [
        (1, 'John Smith', 'john.smith@example.com', '2023-05-15 14:30:00', 118500),
        (3, 'Emily Johnson', 'emily.j@example.com', '2023-06-20 11:15:00', 103000),
        (5, 'Michael Williams', 'michael.w@example.com', '2023-07-10 16:45:00', 240000)
    ]
    
    # Insert purchases
    c.executemany('''INSERT INTO purchases 
                    (car_id, buyer_name, buyer_email, purchase_date, purchase_price)
                    VALUES (?, ?, ?, ?, ?)''', purchases)
    
    conn.commit()
    conn.close()
    print("Successfully added sample data!")

if __name__ == '__main__':
    add_sample_data()
