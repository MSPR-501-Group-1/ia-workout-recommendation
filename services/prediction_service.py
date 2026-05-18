import logging
from libs.make_orange_table import make_orange_table
from services.model_service import ModelService
from libs.exercise_database import db
from models.workoutInputModel import WorkoutInput
from models.predictionResponseModel import PredictionResponse
from libs.build_plan import build_plan

logger = logging.getLogger(__name__)
model_service = ModelService()


class PredictionService:
    
    @staticmethod
    def predict(input_data: WorkoutInput) -> PredictionResponse:
        program_table = make_orange_table(
            model_service.get_program_domain(),
            input_data
        )
        intensity_table = make_orange_table(
            model_service.get_intensity_domain(),
            input_data
        )

        program_pred = model_service.get_program_model()(program_table)
        intensity_pred = model_service.get_intensity_model()(intensity_table)

        recommended_program=model_service.get_program_classes()[int(program_pred[0])]
        recommended_intensity=model_service.get_intensity_classes()[int(intensity_pred[0])]

        exercises = db.filter(
            programs=recommended_program,
            forbidden_injuries=input_data.injury_type + "_" + input_data.injury_severity
        )

        logger.info(f"Exercices filtrés: {len(exercises)} trouvés pour le programme '{recommended_program}' et l'injury interdite '{input_data.injury_type}_{input_data.injury_severity}'")
        plan = build_plan(exercises, input_data.fitness_level, recommended_intensity)

        logger.info(f"Plan d'exercice généré: {len(plan)} exercices recommandés pour le programme '{recommended_program}' à l'intensité '{recommended_intensity}'")

        return PredictionResponse(
            # En plus de retourner le programme brut avec son intensité, on va retourner le plan d'exercice correspondant.
            recommended_program=recommended_program,
            recommended_intensity=recommended_intensity,
            recommended_plan=plan
        )
