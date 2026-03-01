from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, query, users
from app.core.database import engine, Base
from app.core.exceptions import AppException, app_exception_handler, global_exception_handler
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST,Counter, Gauge
from starlette.responses import Response


active_users = Gauge('active_users', 'Number of active users')
rag_pipeline_calls = Counter('rag_pipeline_calls_total', 'Total RAG pipeline calls')
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])

app = FastAPI(title="CliniQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(query.router)
app.include_router(users.router)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    return {"message": "CliniQ API"}
