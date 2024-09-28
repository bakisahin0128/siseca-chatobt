from fastapi import APIRouter


default_router = APIRouter(
    responses={404: dict(status="error", error="Not found", data={})}
)
