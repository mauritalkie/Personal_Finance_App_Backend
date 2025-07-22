from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)