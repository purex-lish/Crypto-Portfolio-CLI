# import requests

# def fetch_top_coins():
#     url = "https://api.coingecko.com/api/v3/coins/markets"
#     params = {
#         'vs_currency': 'usd',
#         'order': 'market_cap_desc',
#         'per_page': 20,
#         'page': 1,
#         'sparkline': False
#     }
    
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Failed to fetch data:", response.status_code)
#         return None
# def exit_program():
#     print("Goodbye!")
#     exit()

# import requests
# from sqlalchemy.orm import sessionmaker
# from .db.models import User, CryptoAsset, UserPortfolio
# from .db.database import engine  # Assuming you have a database setup in a file named database.py

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# def fetch_top_coins():
#     url = "https://api.coingecko.com/api/v3/coins/markets"
#     params = {
#         'vs_currency': 'usd',
#         'order': 'market_cap_desc',
#         'per_page': 20,
#         'page': 1,
#         'sparkline': False
#     }
    
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Failed to fetch data:", response.status_code)
#         return None

# def exit_program():
#     print("Goodbye!")
#     exit()

# def add_to_portfolio(user_id, asset_id, quantity):
#     # Logic to add the asset to the user's portfolio
#     new_portfolio = UserPortfolio(user_id=user_id, asset_id=asset_id, quantity=quantity)
#     session.add(new_portfolio)
#     session.commit()
#     print(f"Added {quantity} of asset ID {asset_id} to user ID {user_id}'s portfolio.")

# def view_user_portfolio():
#     user_id = input("Enter your user ID: ")
#     user = session.query(User).filter_by(id=user_id).first()
#     if user:
#         print(f"Portfolio for {user.username}:")
#         for portfolio in user.portfolios:
#             asset = session.query(CryptoAsset).filter_by(id=portfolio.asset_id).first()
#             print(f"  - {portfolio.quantity} of {asset.name} ({asset.symbol})")
#     else:
#         print("User not found.")
import requests
from sqlalchemy.orm import sessionmaker
from lib.db.models import User, CryptoAsset, UserPortfolio
from lib.db.database import engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def fetch_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 20,
        'page': 1,
        'sparkline': False
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

def exit_program():
    print("Goodbye!")
    session.close()  # Close the session before exiting
    exit()

def add_to_portfolio(user_id, asset_id, quantity):
    user = session.query(User).filter_by(id=user_id).first()
    asset = session.query(CryptoAsset).filter_by(id=asset_id).first()
    
    if not user:
        print("User not found.")
        return
    if not asset:
        print("Asset not found.")
        return
    
    new_portfolio = UserPortfolio(user_id=user_id, asset_id=asset_id, quantity=quantity)
    session.add(new_portfolio)
    session.commit()
    print(f"Added {quantity} of {asset.name} to user {user.username}'s portfolio.")

def view_user_portfolio():
    user_id = input("Enter your user ID: ")
    user = session.query(User).filter_by(id=user_id).first()
    
    if user:
        print(f"Portfolio for {user.username}:")
        for portfolio in user.portfolios:
            asset = session.query(CryptoAsset).filter_by(id=portfolio.asset_id).first()
            if asset:
                print(f"  - {portfolio.quantity} of {asset.name} ({asset.symbol})")
            else:
                print(f"  - {portfolio.quantity} of asset with ID {portfolio.asset_id} (not found)")
    else:
        print("User not found.")
