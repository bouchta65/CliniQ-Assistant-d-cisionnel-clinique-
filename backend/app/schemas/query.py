from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class Query(BaseModel):
    query_text: str
    reponse: str
    created_at: Optional[date] = None  

class QueryCreate(Query):
    pass  

class QueryRead(Query):
    id: int

    model_config = ConfigDict(from_attributes=True)
