import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, User, CryptoAsset

# Replace with your database URL
DATABASE_URL = "sqlite:///crypto_cli.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Fetch top 10 cryptocurrencies
def fetch_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return []

# Create users
user1 = User(username='Mary')
user2 = User(username='Lucy')

# Add users to the session
session.add(user1)
session.add(user2)

# Fetch live crypto assets
crypto_data = fetch_top_coins()

for coin in crypto_data:
    # Create a new CryptoAsset for each coin
    crypto_asset = CryptoAsset(
        name=coin['name'],
        symbol=coin['symbol'].upper(),
        current_price=coin['current_price'],
        market_cap=coin['market_cap'],
        price_change_24h=coin['price_change_percentage_24h']
    )
    session.add(crypto_asset)

# Commit the session
session.commit()
session.close()
