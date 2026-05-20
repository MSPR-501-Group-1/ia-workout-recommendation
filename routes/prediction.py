from fastapi import APIRouter
from controllers.prediction_controller import PredictionController
from models.workoutInputModel import WorkoutInput
from models.predictionResponseModel import PredictionResponse

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(input_data: WorkoutInput):
    print(input_data)
    return await PredictionController.predict(input_data)
