import mysql.connector

# Function to connect to MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",   # Default user in XAMPP MySQL
            password="",   # Leave empty if no password is set
            database="web_enum_tool"
        )
        print("[✅] Connected to Database")  # Debugging message
        return conn
    except mysql.connector.Error as err:
        print("[❌] MySQL Connection Error:", err)
        return None

# Function to initialize database and create 'users' table if it doesn't exist
def initialize_db():
    conn = connect_db()
    if conn is None:
        print("[❌] Database connection failed. Exiting initialization.")
        return

    cursor = conn.cursor()
    try:
        # Create users table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        print("[✅] Users table is ready.")
    except mysql.connector.Error as err:
        print("[❌] Error creating table:", err)
    finally:
        cursor.close()
        conn.close()

# Function to test database connection
if __name__ == "__main__":
    print("Testing Database Connection...")
    conn = connect_db()
    if conn:
        print("[✅] Database Connection Successful!")
        initialize_db()  # Ensure database is set up
        conn.close()
    else:
        print("[❌] Failed to connect to the database.")
