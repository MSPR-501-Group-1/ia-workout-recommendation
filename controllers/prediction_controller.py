import logging
from fastapi import HTTPException
from services.prediction_service import PredictionService
from models.workoutInputModel import WorkoutInput
from models.predictionResponseModel import PredictionResponse

logger = logging.getLogger(__name__)


class PredictionController:

    @staticmethod
    async def predict(input_data: WorkoutInput) -> PredictionResponse:
        try:
            return PredictionService.predict(input_data)
        except Exception as e:
            logger.error(f"Prediction error: {type(e).__name__}: {e}")
            raise HTTPException(status_code=500, detail="Erreur lors de la prédiction")
