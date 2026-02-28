from sqlalchemy import Column, Integer, ForeignKey, Text , DateTime
from backend.app.core.database import Base
class query(Base):
    __tablename__ = "query"
    
    id = Column(Integer, primery_key = True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime, default=DateTime.utcnow)