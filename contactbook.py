import sqlite3
import sys

# Connect to SQLite database
def connect_to_db():
    try:
        connection = sqlite3.connect("phonebook.db")
        print("Database connection successful.")
        return connection
    except Exception as error:
        print(f"Database connection failed: {error}")
        sys.exit(1)

# Create table
def create_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ContactBook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE
            );
        """)
        cursor.connection.commit()
        print("Table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
        cursor.connection.rollback()
        sys.exit(1)

# Insert or update user
def insert_or_update_user(cursor, name, phone):
    try:
        cursor.execute("SELECT id FROM ContactBook WHERE first_name = ?", (name,))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE ContactBook SET phone = ? WHERE first_name = ?", (phone, name))
        else:
            cursor.execute("INSERT INTO ContactBook(first_name, phone) VALUES (?, ?)", (name, phone))
        cursor.connection.commit()
    except Exception as e:
        print(f"Error inserting/updating user: {e}")
        cursor.connection.rollback()

# Search user
def search_phonebook(cursor, pattern):
    cursor.execute("""
        SELECT * FROM ContactBook
        WHERE first_name LIKE ? OR phone LIKE ?
    """, (f"%{pattern}%", f"%{pattern}%"))
    return cursor.fetchall()

def main():
    connection = connect_to_db()
    cursor = connection.cursor()

    create_table(cursor)

    while True:
        print("\n1. Insert or Update Contact")
        print("2. Search Contact")
        print("3. View All Contacts")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            # Insert or update contact
            name = input("Enter contact name: ")
            phone = input("Enter contact phone: ")
            insert_or_update_user(cursor, name, phone)
        
        elif choice == '2':
            # Search contact
            search_pattern = input("Enter search keyword (name or phone): ")
            results = search_phonebook(cursor, search_pattern)
            if results:
                print("\nSearch Results:")
                for row in results:
                    print(row)
            else:
                print("No matching contacts found.")
        
        elif choice == '3':
            # View all contacts
            print("\nCurrent contact book records:")
            cursor.execute("SELECT * FROM ContactBook ORDER BY id;")
            for row in cursor.fetchall():
                print(row)

        elif choice == '4':
            # Exit the program
            break
        else:
            print("Invalid choice. Please select a valid option.")

    cursor.close()
    connection.close()
    print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
