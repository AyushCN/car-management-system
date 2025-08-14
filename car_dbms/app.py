from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    
    # Create cars table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS cars
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  make TEXT NOT NULL,
                  model TEXT NOT NULL,
                  year INTEGER NOT NULL,
                  price REAL NOT NULL,
                  mileage INTEGER,
                  color TEXT,
                  description TEXT,
                  image TEXT,
                  available BOOLEAN DEFAULT 1)''')
    
    # Create purchases table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS purchases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  car_id INTEGER NOT NULL,
                  buyer_name TEXT NOT NULL,
                  buyer_email TEXT NOT NULL,
                  purchase_date TEXT NOT NULL,
                  purchase_price REAL NOT NULL,
                  FOREIGN KEY (car_id) REFERENCES cars(id))''')
    
    conn.commit()
    conn.close()

init_db()
@app.context_processor
def inject_datetime():
    return dict(datetime=datetime)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars')
def cars():
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get filter parameters from URL
    make_filter = request.args.get('make')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    query = "SELECT * FROM cars WHERE available = 1"
    params = []
    
    if make_filter:
        query += " AND make = ?"
        params.append(make_filter)
    if min_price:
        query += " AND price >= ?"
        params.append(float(min_price))
    if max_price:
        query += " AND price <= ?"
        params.append(float(max_price))
    
    c.execute(query, params)
    cars = c.fetchall()
    
    # Get distinct makes for filter dropdown
    c.execute("SELECT DISTINCT make FROM cars WHERE available = 1 ORDER BY make")
    makes = [row['make'] for row in c.fetchall()]
    
    conn.close()
    return render_template('cars.html', cars=cars, makes=makes)

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        mileage = request.form.get('mileage', 0)
        color = request.form.get('color', '')
        description = request.form.get('description', '')
        image = request.form.get('image', 'default.jpg')
        
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('''INSERT INTO cars 
                    (make, model, year, price, mileage, color, description, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (make, model, year, price, mileage, color, description, image))
        conn.commit()
        conn.close()
        
        return redirect(url_for('cars'))
    
    return render_template('add_car.html')

@app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        mileage = request.form.get('mileage', 0)
        color = request.form.get('color', '')
        description = request.form.get('description', '')
        image = request.form.get('image', 'default.jpg')
        available = 1 if request.form.get('available') else 0
        
        c.execute('''UPDATE cars SET 
                    make=?, model=?, year=?, price=?, mileage=?, 
                    color=?, description=?, image=?, available=?
                    WHERE id=?''',
                 (make, model, year, price, mileage, color, 
                  description, image, available, car_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('cars'))
    
    c.execute("SELECT * FROM cars WHERE id=?", (car_id,))
    car = c.fetchone()
    conn.close()
    
    if not car:
        return redirect(url_for('cars'))
    
    return render_template('edit_car.html', car=car)

@app.route('/purchase/<int:car_id>', methods=['GET', 'POST'])
def purchase(car_id):
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM cars WHERE id=?", (car_id,))
    car = c.fetchone()
    
    if not car or not car['available']:
        conn.close()
        return redirect(url_for('cars'))
    
    if request.method == 'POST':
        buyer_name = request.form['buyer_name']
        buyer_email = request.form['buyer_email']
        purchase_price = request.form['purchase_price']
        purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Record purchase
        c.execute('''INSERT INTO purchases 
                    (car_id, buyer_name, buyer_email, purchase_date, purchase_price)
                    VALUES (?, ?, ?, ?, ?)''',
                 (car_id, buyer_name, buyer_email, purchase_date, purchase_price))
        
        # Mark car as sold
        c.execute("UPDATE cars SET available=0 WHERE id=?", (car_id,))
        
        conn.commit()
        conn.close()
        
        return render_template('purchase_success.html', 
                             car=car, 
                             buyer_name=buyer_name,
                             purchase_price=purchase_price)
    
    conn.close()
    return render_template('purchase.html', car=car)

@app.route('/sales')
def sales():
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''SELECT purchases.*, cars.make, cars.model, cars.year 
                FROM purchases 
                JOIN cars ON purchases.car_id = cars.id
                ORDER BY purchase_date DESC''')
    sales = c.fetchall()
    
    # Calculate total sales
    c.execute("SELECT SUM(purchase_price) FROM purchases")
    total_sales = c.fetchone()[0] or 0
    
    conn.close()
    return render_template('sales.html', sales=sales, total_sales=total_sales)

if __name__ == '__main__':
    app.run(debug=True)
