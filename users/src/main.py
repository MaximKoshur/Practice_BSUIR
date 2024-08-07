from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

from .users.routers import user_router

app = FastAPI(title="PracticeBSUIR", description="Beltekabel")

main_router = APIRouter()

main_router.include_router(user_router, prefix="/users", tags=["users"])

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
