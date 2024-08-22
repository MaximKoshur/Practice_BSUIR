from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

from .cables.routers import Cables_router, Type_router, Mark_router, News_router

app = FastAPI(title="PracticeBSUIR", description="Beltekabel")

main_router = APIRouter()

main_router.include_router(Cables_router, prefix="/Cables", tags=["Cables"])
main_router.include_router(Type_router, prefix="/Type", tags=["Type"])
main_router.include_router(Mark_router, prefix="/Mark", tags=["Mark"])
main_router.include_router(News_router, prefix="/News", tags=["News"])

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
