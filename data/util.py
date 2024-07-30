from typing import Union

import streamlit as st
from sqlalchemy import text
from streamlit.connections import SQLConnection

CONNECTION_NAME = "sqlite-db"
DB_URL = "sqlite:///data/data.sqlite"
VALID_TABLE_NAMES = [
    "locations",
    "bookings",
]

def get_connection() -> SQLConnection:
    return st.connection(
        CONNECTION_NAME,
        url=DB_URL,
        type="sql",
    )

from typing import Union
from sqlalchemy.sql import text
from streamlit.connections import SQLConnection

CONNECTION_NAME = "sqlite-db"
DB_URL = "sqlite:///data/data.sqlite"
VALID_TABLE_NAMES = [
    "locations",
    "bookings",
    "feedback",
    "Sales",
    "customers",
    "ratings",
    "invoicing",
    "payment_info",
    "restaurants",
    "credit_card",
    "credit_limits"
]

def reset_table(conn: SQLConnection, table_name: str) -> Union[None, str]:
    if table_name not in VALID_TABLE_NAMES:
        errmsg = f"Invalid table name. Must choose from: {', '.join(VALID_TABLE_NAMES)}"
        raise RuntimeError(errmsg)

    with conn.session as s:
        if table_name == "locations":
            s.execute("DROP TABLE IF EXISTS locations;")
            s.execute("CREATE TABLE IF NOT EXISTS locations (id INTEGER PRIMARY KEY, city TEXT, suburb TEXT);")
            s.execute("DELETE FROM locations;")
            locations = [
                {"id": 1, "city": "Auckland", "suburb": "NULL"},
                {"id": 2, "city": "Auckland", "suburb": "Arch Hill"},
                {"id": 3, "city": "Auckland", "suburb": "Devonport"},
                {"id": 4, "city": "Auckland", "suburb": "Takapuna"},
                {"id": 5, "city": "Auckland", "suburb": "Parnell"},
                {"id": 6, "city": "Auckland", "suburb": "Ponsonby"},
                {"id": 7, "city": "Auckland", "suburb": "Auckland CBD"},

                {"id": 8, "city": "Wellington", "suburb": "NULL"},
                {"id": 9, "city": "Wellington", "suburb": "Te Aro"},
                {"id": 10, "city": "Wellington", "suburb": "Thorndon"},
                {"id": 11, "city": "Wellington", "suburb": "Mount Victoria"},
                {"id": 12, "city": "Wellington", "suburb": "Wellington CBD"},
                {"id": 13, "city": "Wellington", "suburb": "Kapiti"},

                {"id": 14, "city": "Christchurch", "suburb": "Addington"},
                {"id": 15, "city": "Christchurch", "suburb": "Aranui"},
                {"id": 16, "city": "Christchurch", "suburb": "Riccarton"},
                {"id": 17, "city": "Christchurch", "suburb": "Merivale"},
            ]
            s.execute(text("INSERT INTO locations (id, city, suburb) VALUES (:id, :city, :suburb)"), locations)

        elif table_name == "restaurants":
            s.execute("DROP TABLE IF EXISTS restaurants;")
            s.execute("""
                CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY, name TEXT, location_id INTEGER, FOREIGN KEY(location_id) REFERENCES locations(id));""")
            s.execute("DELETE FROM restaurants;")
            s.execute("""
                SELECT bookings.id, restaurants.name, bookings.location_id, bookings.booking_date
                FROM bookings
                JOIN restaurants ON bookings.restaurant_id = restaurants.id;
            """)

            restaurants = [
                {"id": 1, "name": "The Auckland Eatery", "location_id": 1},
                {"id": 2, "name": "Arch Hill Diner", "location_id": 2},
                {"id": 3, "name": "Devonport Delights", "location_id": 3},
                {"id": 4, "name": "Takapuna Tastes", "location_id": 4},
                {"id": 5, "name": "Parnell Pizzeria", "location_id": 5},
                {"id": 6, "name": "Ponsonby Pasta", "location_id": 6},
                {"id": 7, "name": "CBD Cuisine", "location_id": 7},
                {"id": 8, "name": "Wellington Waffles", "location_id": 8},
                {"id": 9, "name": "Te Aro Tacos", "location_id": 9},
                {"id": 10, "name": "Thorndon Thali", "location_id": 10},
                {"id": 11, "name": "Victoria Vegan", "location_id": 11},
                {"id": 12, "name": "CBD Cafe", "location_id": 12},
                {"id": 13, "name": "Kapiti Kitchen", "location_id": 13},
                {"id": 14, "name": "Addington Appetizers", "location_id": 14},
                {"id": 15, "name": "Aranui Asian", "location_id": 15},
                {"id": 16, "name": "Riccarton Ribs", "location_id": 16},
                {"id": 17, "name": "Merivale Mexican", "location_id": 17},
]
            s.execute(text("INSERT INTO restaurants (id, name, location_id) VALUES (:id, :name, :location_id)"), restaurants)


        elif table_name == "bookings":
            s.execute("DROP TABLE IF EXISTS bookings;")
            s.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY,
                    restaurant_id INTEGER,
                    location_id INTEGER,
                    booking_date DATE,
                    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id),
                    FOREIGN KEY(location_id) REFERENCES locations(id)
                );
            """)
            s.execute("DELETE FROM bookings;")

            bookings = [
                {"id": 1, "restaurant_id": 1, "location_id": 1, "booking_date": "2024-06-01"},
                {"id": 2, "restaurant_id": 2, "location_id": 2, "booking_date": "2024-06-02"},
            ]
            s.execute(text("INSERT INTO bookings (id, restaurant_id, location_id, booking_date) VALUES (:id, :restaurant_id, :location_id, :booking_date)"), bookings)

        
        elif table_name == "feedback":
            s.execute("CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, user_id INTEGER, type TEXT, feedback TEXT);")
            s.execute("DELETE FROM feedback;")
            feedbacks = [
                {"id": 1, "user_id": 1, "type": "Host", "feedback": "Great host!"},
                {"id": 2, "user_id": 2, "type": "Tenant", "feedback": "Nice tenant!"},
            ]
            s.execute(text("INSERT INTO feedback (id, user_id, type, feedback) VALUES (:id, :user_id, :type, :feedback)"), feedbacks)
        elif table_name == "Sales":
            s.execute("DROP TABLE IF EXISTS Sales;")
            s.execute("""
            CREATE TABLE IF NOT EXISTS Sales (
                restaurant_id INTEGER,
                date DATE,
                sales_amount INTEGER,
                PRIMARY KEY (restaurant_id, date)
            );
            """)
            s.execute("DELETE FROM Sales;")
            sales = [
                {"restaurant_id": 1, "date": "2024-01-01", "sales_amount": 5000},
                {"restaurant_id": 2, "date": "2024-01-01", "sales_amount": 4000},
                {"restaurant_id": 3, "date": "2024-01-01", "sales_amount": 6000},
                {"restaurant_id": 4, "date": "2024-01-01", "sales_amount": 5200},
                {"restaurant_id": 5, "date": "2024-01-01", "sales_amount": 5700},
                {"restaurant_id": 6, "date": "2024-01-01", "sales_amount": 5300},
                {"restaurant_id": 7, "date": "2024-01-01", "sales_amount": 4900},
                {"restaurant_id": 8, "date": "2024-01-01", "sales_amount": 5600},
                {"restaurant_id": 9, "date": "2024-01-01", "sales_amount": 4800},
                {"restaurant_id": 10, "date": "2024-01-01", "sales_amount": 4600},
                {"restaurant_id": 11, "date": "2024-01-01", "sales_amount": 5200},
                {"restaurant_id": 12, "date": "2024-01-01", "sales_amount": 5000},
                {"restaurant_id": 13, "date": "2024-01-01", "sales_amount": 4700},
                {"restaurant_id": 14, "date": "2024-01-01", "sales_amount": 4600},
                {"restaurant_id": 15, "date": "2024-01-01", "sales_amount": 5300},
                {"restaurant_id": 16, "date": "2024-01-01", "sales_amount": 4900},
                {"restaurant_id": 17, "date": "2024-01-01", "sales_amount": 5100}
            ]
            s.execute("INSERT INTO Sales (restaurant_id, date, sales_amount) VALUES (:restaurant_id, :date, :sales_amount);", sales)

        elif table_name == "customers":
            s.execute("DROP TABLE IF EXISTS Customers;")
            s.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                restaurant_id INTEGER,
                date DATE,
                number_of_customers INTEGER,
                PRIMARY KEY (restaurant_id, date)
            );
            """)
            s.execute("DELETE FROM Customers;")
            customers = [
                {"restaurant_id": 1, "date": "2024-01-02", "number_of_customers": 160},
                {"restaurant_id": 2, "date": "2024-01-01", "number_of_customers": 120},
                {"restaurant_id": 3, "date": "2024-01-01", "number_of_customers": 180},
                {"restaurant_id": 4, "date": "2024-01-02", "number_of_customers": 170},
                {"restaurant_id": 5, "date": "2024-01-02", "number_of_customers": 180},
                {"restaurant_id": 6, "date": "2024-01-01", "number_of_customers": 140},
                {"restaurant_id": 7, "date": "2024-01-01", "number_of_customers": 130},
                {"restaurant_id": 8, "date": "2024-01-02", "number_of_customers": 170},
                {"restaurant_id": 9, "date": "2024-01-02", "number_of_customers": 150},
                {"restaurant_id": 10, "date": "2024-01-01", "number_of_customers": 130},
                {"restaurant_id": 11, "date": "2024-01-01", "number_of_customers": 150},
                {"restaurant_id": 12, "date": "2024-01-01", "number_of_customers": 140},
                {"restaurant_id": 13, "date": "2024-01-01", "number_of_customers": 130},
                {"restaurant_id": 14, "date": "2024-01-01", "number_of_customers": 130},
                {"restaurant_id": 15, "date": "2024-01-01", "number_of_customers": 140},
                {"restaurant_id": 16, "date": "2024-01-01", "number_of_customers": 130},
                {"restaurant_id": 17, "date": "2024-01-02", "number_of_customers": 140},
            ]
            s.execute("INSERT INTO Customers (restaurant_id, date, number_of_customers) VALUES (:restaurant_id, :date, :number_of_customers);", customers)

        elif table_name == "ratings":
            # Create Ratings Table
            s.execute("DROP TABLE IF EXISTS Ratings;")
            s.execute("""
            CREATE TABLE IF NOT EXISTS Ratings (
                restaurant_id INTEGER,
                date DATE,
                rating REAL,
                PRIMARY KEY (restaurant_id, date)
            );
            """)
            s.execute("DELETE FROM Ratings;")
            ratings = [
                {"restaurant_id": 1, "date": "2024-01-02", "rating": 4.6},
                {"restaurant_id": 2, "date": "2024-01-01", "rating": 4.2},
                {"restaurant_id": 3, "date": "2024-01-01", "rating": 4.7},
                {"restaurant_id": 4, "date": "2024-01-01", "rating": 4.6},
                {"restaurant_id": 5, "date": "2024-01-02", "rating": 4.9},
                {"restaurant_id": 6, "date": "2024-01-01", "rating": 4.3},
                {"restaurant_id": 7, "date": "2024-01-01", "rating": 4.5},
                {"restaurant_id": 8, "date": "2024-01-02", "rating": 4.8},
                {"restaurant_id": 9, "date": "2024-01-02", "rating": 4.5},
                {"restaurant_id": 10, "date": "2024-01-02", "rating": 4.4},
                {"restaurant_id": 11, "date": "2024-01-01", "rating": 4.6},
                {"restaurant_id": 12, "date": "2024-01-01", "rating": 4.5},
                {"restaurant_id": 13, "date": "2024-01-02", "rating": 4.5},
                {"restaurant_id": 14, "date": "2024-01-02", "rating": 4.4},
                {"restaurant_id": 15, "date": "2024-01-01", "rating": 4.5},
                {"restaurant_id": 16, "date": "2024-01-02", "rating": 4.5},
                {"restaurant_id": 17, "date": "2024-01-01", "rating": 4.4},
            ]
            s.execute("INSERT INTO Ratings (restaurant_id, date, rating) VALUES (:restaurant_id, :date, :rating);", ratings)
        elif table_name == "invoicing":
            s.execute("DROP TABLE IF EXISTS invoicing;")
            s.execute("CREATE TABLE IF NOT EXISTS invoicing (id INTEGER PRIMARY KEY, status TEXT);")
            s.execute("DELETE FROM invoicing;")
            invoicing = [
                {"id": 1, "status": "Paid"},
                {"id": 2, "status": "Unpaid"},
            ]
            s.execute(text("INSERT INTO invoicing (id, status) VALUES (:id, :status)"), invoicing)
        elif table_name == "payment_info":
            s.execute("DROP TABLE IF EXISTS payment_info;")
            s.execute("CREATE TABLE IF NOT EXISTS payment_info (user_id INTEGER PRIMARY KEY, payment_method TEXT, automatic_payments BOOLEAN);")
            s.execute("DELETE FROM payment_info;")
            payment_info = [
                {"user_id": 1, "payment_method": "Credit Card", "automatic_payments": True},
                {"user_id": 2, "payment_method": "Internet Banking", "automatic_payments": False},
            ]
            s.execute(text("INSERT INTO payment_info (user_id, payment_method, automatic_payments) VALUES (:user_id, :payment_method, :automatic_payments)"), payment_info)
        elif table_name == "credit_card":
            s.execute("DROP TABLE IF EXISTS credit_card;")
            s.execute("CREATE TABLE IF NOT EXISTS credit_card (user_id INTEGER PRIMARY KEY, card_number TEXT, expiry_date TEXT, cvv TEXT);")
            s.execute("DELETE FROM credit_card;")
            credit_card = [
                {"user_id": 1, "card_number": "1234567812345678", "expiry_date": "01/23", "cvv": "123"},
            ]
            s.execute(text("INSERT INTO credit_card (user_id, card_number, expiry_date, cvv) VALUES (:user_id, :card_number, :expiry_date, :cvv)"), credit_card)
        elif table_name == "credit_limits":
            s.execute("DROP TABLE IF EXISTS credit_limits;")
            s.execute('CREATE TABLE IF NOT EXISTS credit_limits (id TEXT PRIMARY KEY, "limit" REAL);')
            
            credit_limits = [
                {"id": "1", "limit": 1000.0},
            ]
            
            for credit_limit in credit_limits:
                existing = s.execute(text('SELECT * FROM credit_limits WHERE id = :id'), {"id": credit_limit["id"]}).fetchone()
                if existing is None:
                    s.execute(text('INSERT INTO credit_limits (id, "limit") VALUES (:id, :limit)'), credit_limit)
                else:
                    s.execute(text('UPDATE credit_limits SET "limit" = :limit WHERE id = :id'), credit_limit)


        s.commit()


