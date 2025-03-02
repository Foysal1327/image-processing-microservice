import os
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_FILE = "data/image_data.db"
DB_URL = f"sqlite:///{DB_FILE}"


engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


if not os.path.exists("data"):
    os.makedirs("data")


class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False) 
    time_frames = Column(Integer, nullable=False)
    channels = Column(Integer, nullable=False)
    dtype = Column(String, nullable=False)

class ImageAnalysis(Base):
    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    pca_components = Column(Integer, nullable=True)
    statistics = Column(JSON, nullable=True) 

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

