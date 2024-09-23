#Import classes from your models
from lib.db.models import User, CryptoAsset, UserPortfolio
from lib.db.database import SessionLocal, engine, init_db