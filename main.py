import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from routes.prediction import router
from services.model_service import ModelService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_service = ModelService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_service.load_models()
    yield


tags_metadata = [
    {
        "name": "Prediction",
        "description": "Endpoints de recommandation d'entraînement.",
    },
    {
        "name": "System",
        "description": "Endpoints système et de santé.",
    },
]

app = FastAPI(
    title="Fitness AI Coach API",
    description=(
        "API pour recommandation d'entraînement basée sur ML."
        " Fournit un programme, une intensité et un plan d'exercices."
    ),
    version="1.0.0",
    contact={
        "name": "HealthAI Team",
        "email": "support@healthai.local",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["System"], summary="Health check")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

