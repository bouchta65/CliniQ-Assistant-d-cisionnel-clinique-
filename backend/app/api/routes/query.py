from app.core.database import get_db
from app.core.exceptions import AppException
from app.schemas.query import QueryCreate
from app.services.assistant_service import generate, generate_and_evaluate
from app.services.query_service import (
    create_query,
    delete_query,
    get_all_query,
    get_queries_by_user_id,
    get_query_by_id,
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/assistant")
def query_root(query: QueryCreate, db: Session = Depends(get_db)):
    try:
        ai_response = generate(query.query_text, evaluate=True)
        saved = create_query(db, query.query_text, ai_response, query.user_id)

        return {"question": query.query_text, "answer": ai_response, "db_id": saved.id}
    except Exception as e:
        raise AppException(str(e))


@router.post("/assistant/evaluate")
def query_evaluate(query: QueryCreate, db: Session = Depends(get_db)):
    try:
        answer, metrics = generate_and_evaluate(query.query_text, k=5)
        saved = create_query(db, query.query_text, answer, query.user_id)

        return {
            "question": query.query_text,
            "answer": answer,
            "metrics": metrics,
            "db_id": saved.id,
        }
    except Exception as e:
        raise AppException(str(e))


@router.get("/queries")
def get_queries(db: Session = Depends(get_db)):
    return get_all_query(db)


@router.get("/queries/{query_id}")
def get_query(query_id: int, db: Session = Depends(get_db)):
    return get_query_by_id(db, query_id)


@router.delete("/queries/{query_id}")
def delete_query_by_id(query_id: int, db: Session = Depends(get_db)):
    return delete_query(db, query_id)


@router.get("/queries/user/{user_id}")
def get_user_queries(user_id: int, db: Session = Depends(get_db)):
    return get_queries_by_user_id(db, user_id)
