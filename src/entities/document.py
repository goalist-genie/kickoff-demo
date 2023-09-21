from sqlalchemy import Column, Integer, String
from database import BaseEntity

class Document(BaseEntity):
    __tablename__ = "documents"
    