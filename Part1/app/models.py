from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class MalwareURL(Base):
    __tablename__ = "malware_urls"

    id = Column(Integer, primary_key=True, index=True)
    url_identifier = Column(String, unique=True, index=True) 
    is_malware = Column(Boolean, default=True)