from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from app.core.database import get_db
from app.schemas.query import QueryCreate
from app.services.query_service import create_query, get_all_query, get_query_by_id, delete_query
from app.services.assistant_service import generate
from app.core.exceptions import AppException

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/assistant")
def query_root(query: QueryCreate, db: Session = Depends(get_db)):
    try:
        ai_response = generate(query.query_text)
        saved = create_query(db, query.query_text, ai_response, query.user_id)
        
        return {
            "question": query.query_text,
            "answer": ai_response,
            "db_id": saved.id
        }
    except Exception as e:
        raise AppException(str(e))

@router.get("/queries")
def get_queries(db: Session = Depends(get_db)):
    return get_all_query(db)

@router.get("/queries/{query_id}")
def get_query(query_id: int, db: Session = Depends(get_db)):
    return get_query_by_id(db, query_id)

