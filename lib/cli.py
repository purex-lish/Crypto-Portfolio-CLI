import sqlite3
from lib.helpers import (
    exit_program,
    fetch_top_coins,
    add_to_portfolio,
    view_user_portfolio
)

def create_tables():
    """Create necessary tables if they don't exist."""
    conn = sqlite3.connect('crypto_cli.db')
    cursor = conn.cursor()
    
    # Create cryptocurrencies table
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS cryptocurrencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            symbol TEXT NOT NULL,
            current_price REAL NOT NULL,
            market_cap REAL NOT NULL,
            price_change_percentage_24h REAL NOT NULL
        )
    """)
    
    # Create users table with a unique username
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)
    
    # Create user portfolios table to track user holdings
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS user_portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cryptocurrency_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (cryptocurrency_id) REFERENCES cryptocurrencies (id)
        )
    """)
    
    conn.commit()
    conn.close()

def main():
    create_tables()  # Ensure the tables exist
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            display_top_coins()
        elif choice == "2":
            view_user_portfolio()
        elif choice == "3":
            add_crypto_to_portfolio()
        elif choice == "4":
            display_db_data()  # Display cryptocurrency data
        elif choice == "5":
            list_tables()  # List all tables in the database
        elif choice == "6":
            register_user()  # Option for user registration
        else:
            print("Invalid choice, please try again.")

def menu():
    """Display the main menu options to the user."""
    print("\nPlease select an option:")
    print("0. Exit the program")
    print("1. Get top 20 cryptocurrencies")
    print("2. View user portfolio")
    print("3. Add cryptocurrency to portfolio")
    print("4. Display data from crypto_cli.db")
    print("5. List database tables")
    print("6. Register a new user")

def register_user():
    """Register a new user by storing their username in the database."""
    username = input("Enter a username: ")

    conn = sqlite3.connect('crypto_cli.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    except Exception as e:
        print(f"Error registering user: {e}")
    finally:
        conn.close()

def display_top_coins():
    """Fetch and display the top 20 cryptocurrencies."""
    top_coins = fetch_top_coins()
    if top_coins:
        insert_top_coins_to_db(top_coins)  # Insert data into the database

        print("\nTop 20 Cryptocurrencies:")
        print("{:<4} {:<20} {:<10} {:<15} {:<15} {:<15}".format("Rank", "Name", "Symbol", "Price (USD)", "Market Cap", "24h Change"))
        print("-" * 80)
        
        for index, coin in enumerate(top_coins):
            rank = index + 1
            name = coin['name']
            symbol = coin['symbol'].upper()
            price = coin['current_price']
            market_cap = coin['market_cap']
            price_change_24h = coin['price_change_percentage_24h']

            market_cap_display = format_market_cap(market_cap)

            print("{:<4} {:<20} {:<10} ${:<14,.2f} {:<14} {:>10.2f}%".format(
                rank, name, symbol, price, market_cap_display, price_change_24h))
    else:
        print("Failed to retrieve coin data.")
    print()

def insert_top_coins_to_db(top_coins):
    """Insert top coins into the cryptocurrencies table, avoiding duplicates."""
    conn = sqlite3.connect('crypto_cli.db')
    cursor = conn.cursor()
    
    for coin in top_coins:
        name = coin['name']
        symbol = coin['symbol']
        current_price = coin['current_price']
        market_cap = coin['market_cap']
        price_change_24h = coin['price_change_percentage_24h']

        # Check for duplicates before inserting
        cursor.execute("SELECT * FROM cryptocurrencies WHERE symbol = ?", (symbol,))
        if cursor.fetchone() is None:  # If the coin is not in the database
            cursor.execute(""" 
                INSERT INTO cryptocurrencies (name, symbol, current_price, market_cap, price_change_percentage_24h)
                VALUES (?, ?, ?, ?, ?)
            """, (name, symbol, current_price, market_cap, price_change_24h))
    
    conn.commit()
    conn.close()
    print("Top cryptocurrencies have been added to the database.")

def display_db_data():
    """Display cryptocurrency data stored in the database."""
    conn = sqlite3.connect('crypto_cli.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, symbol, current_price, market_cap, price_change_percentage_24h FROM cryptocurrencies")
    rows = cursor.fetchall()
    
    print("\nCryptocurrency Data from Database:")
    print("{:<20} {:<10} {:<15} {:<15} {:<15}".format("Name", "Symbol", "Price (USD)", "Market Cap", "24h Change"))
    print("-" * 80)
    
    for row in rows:
        name, symbol, price, market_cap, price_change_24h = row
        market_cap_display = format_market_cap(market_cap)

        print("{:<20} {:<10} ${:<14,.2f} {:<14} {:>10.2f}%".format(
            name, symbol.upper(), price, market_cap_display, price_change_24h))
    
    conn.close()
    print()  # Newline for better readability

def format_market_cap(market_cap):
    """Format market cap into human-readable format."""
    if market_cap >= 1_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f}B"
    elif market_cap >= 1_000_000:
        return f"${market_cap / 1_000_000:.2f}M"
    else:
        return f"${market_cap:.2f}"

def list_tables():
    """List all tables in the database."""
    conn = sqlite3.connect('crypto_cli.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\nTables in database:")
    for table in tables:
        print(table[0])
    
    conn.close()
    print()

def add_crypto_to_portfolio():
    """Add a cryptocurrency to a user's portfolio."""
    username = input("Enter your username: ")
    asset_symbol = input("Enter the asset symbol of the cryptocurrency: ")
    
    try:
        quantity = float(input("Enter the quantity: "))
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return
    except ValueError:
        print("Invalid quantity. Please enter a number.")
        return
    
    conn = sqlite3.connect('crypto_cli.db')
    cursor = conn.cursor()
    
    # Get user ID from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user is None:
        print("User not found.")
        conn.close()
        return

    user_id = user[0]

    # Get cryptocurrency ID from symbol
    cursor.execute("SELECT id FROM cryptocurrencies WHERE symbol = ?", (asset_symbol,))
    crypto = cursor.fetchone()
    
    if crypto is None:
        print("Cryptocurrency not found.")
        conn.close()
        return
    
    cryptocurrency_id = crypto[0]

    try:
        # Insert into user portfolios
        cursor.execute(""" 
            INSERT INTO user_portfolios (user_id, cryptocurrency_id, quantity)
            VALUES (?, ?, ?)
        """, (user_id, cryptocurrency_id, quantity))
        conn.commit()
        print("Crypto asset added to your portfolio.")
    except Exception as e:
        print(f"Error adding to portfolio: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
