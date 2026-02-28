from sqlalchemy.orm import Session
from app.models.query import Query
from app.schemas.query import QueryCreate

def create_query(db: Session, query_text: str, response: str, user_id: int):
    db_query = Query(
        query=query_text,
        response=response,
        user_id=user_id,     
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

def delete_query(db: Session, query_id: int):
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        return {"error": "Query not found"}
    db.delete(query)
    db.commit()
    return {"message": "Query deleted successfully"}

def get_query_by_id(db: Session, query_id: int):
    return db.query(Query).filter(Query.id == query_id).first()

def get_all_query(db: Session):
    return db.query(Query).all()
    
    
    
    
    