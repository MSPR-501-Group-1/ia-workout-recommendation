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


app = FastAPI(
    title="Fitness AI Coach API",
    description="API pour recommandation d'entraînement basée sur ML",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

