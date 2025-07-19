from sqlalchemy import Column, Integer, String, Float, Date
from app.db.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String, index=True)
    amount = Column(Float)
    date = Column(Date)
    category = Column(String)
