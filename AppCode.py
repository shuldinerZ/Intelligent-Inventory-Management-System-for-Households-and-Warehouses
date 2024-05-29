import cv2
from pyzbar.pyzbar import decode
import sqlite3

def initialize_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (barcode TEXT, name TEXT, expiration_date TEXT)''')
    conn.commit()
    conn.close()

def add_product(barcode, name, expiration_date):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (barcode, name, expiration_date) VALUES (?, ?, ?)",
              (barcode, name, expiration_date))
    conn.commit()
    conn.close()

def scan_barcode(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f"Barcode detected: {barcode_data}")
        return barcode_data
    return None

def main():
    initialize_db()
    
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        barcode_data = scan_barcode(frame)
        if barcode_data:
            product_name = input("Enter product name: ")
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            add_product(barcode_data, product_name, expiration_date)
            print(f"Product {product_name} added to the inventory.")
        
        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
