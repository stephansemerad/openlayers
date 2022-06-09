from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime, Float, MetaData
from sqlalchemy.orm import relationship
from datetime import datetime
import os


DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    type = Column(String(255))
    price = Column(Numeric)
    area = Column(Numeric)
    lon = Column(Float)
    lat = Column(Float)
    url = Column(String(255))

    # source_id = Column(String(255))
    # source_url = Column(String(255))
    # seller = Column(String(255))
    # seller_tel = Column(String(255))
    # seller_email = Column(String(255))
    
    
    def as_dict(self):
        dictionary = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dictionary['lat'] = float(self.lat)
        dictionary['lon'] = float(self.lon)
        return dictionary


print("creating schema")
Base.metadata.create_all(engine)
