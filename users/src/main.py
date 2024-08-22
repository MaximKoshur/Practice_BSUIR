from fastapi import FastAPI
from fastapi.routing import APIRouter
import uvicorn

from .users.routers import user_router, vacancy_router, application_roter, tokens_roter

app = FastAPI(title="PracticeBSUIR", description="Beltekabel")

main_router = APIRouter()

main_router.include_router(tokens_roter, prefix="/tokens", tags=["Tokens"])
main_router.include_router(user_router, prefix="/users", tags=["Users"])
main_router.include_router(vacancy_router, prefix="/vacancies", tags=["Vacancies"])
main_router.include_router(application_roter, prefix="/applications", tags=["Applications"])


app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
