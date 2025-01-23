import os
from getpass import getpass
import psycopg2

from decouple import config


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class TerminalBusSimulator:
    def __init__(self):
        self.db_conn = self.connect_db()

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='bus_terminal',
                user='postgres',
                password='Ziba11107879'
            )
            return conn
        except psycopg2.DatabaseError as e:
            print(f"Database connection error: {e}")
        except Exception as e:
            print(f"Database connection error: {e}")

    def create_tables(self):
        with self.db_conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                credit INTEGER DEFAULT 0
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id SERIAL PRIMARY KEY,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                cost INTEGER NOT NULL,
                active BOOLEAN DEFAULT TRUE
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users (id),
                trip_id INTEGER REFERENCES trips (id),
                purchase_time TIMESTAMP NOT NULL
            );
            """)
            self.db_conn.commit()

    def signup(self):
        clear_screen()
        print("User Signup")
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        try:
            with self.db_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, password)
                )
                self.db_conn.commit()
                print("Signup successful!")
        except Exception as e:
            print(f"Error during signup: {e}")

    def login(self):
        clear_screen()
        print("User Login")
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        try:
            with self.db_conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM users WHERE username = %s AND password = %s",
                    (username, password)
                )
                user = cur.fetchone()
                if user:
                    print("Login successful!")
                    return user[0]
                else:
                    print("Invalid username or password!")
        except Exception as e:
            print(f"Error during login: {e}")
        return None
    

    def admin_dashboard(self):
        while True:
            clear_screen()
            print("Admin Dashboard")
            print("1. Create Trip")
            print("2. View Trips")
            print("3. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_trip()
            elif choice == "2":
                self.view_trips()
            elif choice == "3":
                break
            input("Press Enter to continue...")

    def create_trip(self):
        clear_screen()
        print("Create New Trip")
        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
        cost = int(input("Enter cost: "))

        try:
            with self.db_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO trips (start_time, end_time, cost, active) VALUES (%s, %s, %s, TRUE)",
                    (start_time, end_time, cost)
                )
            self.db_conn.commit()
            print("Trip created successfully!")
        except Exception as e:
            print(f"Error creating trip: {e}")
  
    def view_trips(self):
        try:
            with self.db_conn.cursor() as cur:
                cur.execute("SELECT * FROM trips WHERE active = TRUE")
                trips = cur.fetchall()
                for trip in trips:
                    print(trip)
        except Exception as e:
            print(f"Error viewing trips: {e}")


if __name__ == "__main__":
    simulator = TerminalBusSimulator()
    simulator.create_tables()

    superuser_username = "admin"
    superuser_password = "password"  

    while True:
        clear_screen()
        print("Welcome to Terminal Bus Simulator")
        print("1. Signup")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            simulator.signup()
        elif choice == "2":
            user_id = simulator.login()
            if user_id:
                print("User ID:", user_id) 
        elif choice == "3":
            clear_screen()
            print("Admin Login")
            username = input("Enter username: ")
            password = getpass("Enter password: ")

            if username == superuser_username and password == superuser_password:
                simulator.admin_dashboard()
            else:
                print("Invalid admin credentials!")
        elif choice == "4":
            break
        input("Press Enter to continue...")  