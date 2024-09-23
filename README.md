#Phase 3 Project
Crypto Portfolio CLI
A command-line interface (CLI) application for managing a cryptocurrency portfolio built using SQLAlchemy, a Python SQL toolkit and Object-Relational Mapping (ORM) library. This application allows users to register, view their portfolios, and track various cryptocurrencies.

Features
User Registration: Users can create an account with a unique username.
Portfolio Management: Users can add cryptocurrencies to their portfolios.
Data Display: View the top 20 cryptocurrencies, along with their prices and market data.
Database Management: SQLite is used for persistent storage of user data and cryptocurrency information.
Prerequisites
Python 3.8 or higher
SQLite
Installation
Clone the repository:

bash
git clone https://github.com/yourusername/crypto-portfolio-cli.git
cd crypto-portfolio-cli
Install required packages: You may want to create a virtual environment before installing dependencies:

bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Usage
Run the application:

bash
python main.py
Main Menu Options:

0: Exit the program
1: Get top 20 cryptocurrencies
2: View user portfolio
3: Add cryptocurrency to portfolio
4: Display data from the database
5: List database tables
6: Register a new user
Register a User: Enter a unique username when prompted.

Add Cryptocurrencies: Input the asset symbol (e.g., BTC for Bitcoin) and the quantity you wish to add to your portfolio.

Database Structure
The application uses SQLite with the following tables:

users: Stores user information.
cryptocurrencies: Stores cryptocurrency data.
user_portfolios: Links users to their owned cryptocurrencies.


Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

Acknowledgments
SQLite for lightweight database management.
Crypto APIs for real-time cryptocurrency data (Coingecko).
