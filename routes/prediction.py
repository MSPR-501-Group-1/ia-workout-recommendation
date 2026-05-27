from fastapi import APIRouter
from controllers.prediction_controller import PredictionController
from models.workoutInputModel import WorkoutInput
from models.predictionResponseModel import PredictionResponse

router = APIRouter(tags=["Prediction"])

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Prédire un programme et une intensité",
    description=(
        "Calcule un programme d'entraînement, une intensité,"
        " et un plan d'exercices basé sur les informations utilisateur."
    ),
    responses={
        200: {"description": "Recommandation calculée"},
        422: {"description": "Erreur de validation"},
        500: {"description": "Erreur interne"},
    },
)
async def predict(input_data: WorkoutInput):
    return await PredictionController.predict(input_data)
