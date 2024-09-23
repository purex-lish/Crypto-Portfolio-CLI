
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    portfolios = relationship("UserPortfolio", back_populates="user")

class CryptoAsset(Base):
    __tablename__ = 'crypto_assets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    symbol = Column(String, unique=True, nullable=False)
    current_price = Column(Float, nullable=False)
    market_cap = Column(Float)
    price_change_24h = Column(Float)
    portfolios = relationship("UserPortfolio", back_populates="crypto_asset")

class UserPortfolio(Base):
    __tablename__ = 'user_portfolios'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    asset_id = Column(Integer, ForeignKey('crypto_assets.id'), nullable=False)
    quantity = Column(Float, nullable=False)

    user = relationship("User", back_populates="portfolios")
    crypto_asset = relationship("CryptoAsset", back_populates="portfolios")
