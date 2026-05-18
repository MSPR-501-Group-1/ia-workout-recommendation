"""
Microservice FastAPI pour recommandation d'entraînement.
Utilise deux modèles de réseau de neurones pour prédire le programme et l'intensité.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Optional, Literal
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from Orange.data import Table

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# INITIALISATION
# ============================================================================

app = FastAPI(
    title="Fitness AI Coach API",
    description="API pour recommandation d'entraînement basée sur ML",
    version="1.0.0"
)

# Charger les modèles
BASE_DIR = Path(__file__).parent
program_model = None
intensity_model = None
program_classes = None
intensity_classes = None


def load_models():
    """Charger les deux modèles au démarrage."""
    global program_model, intensity_model, program_classes, intensity_classes
    try:
        with open(BASE_DIR / "Neural_network_program_model_MSPR.pkcls", "rb") as f:
            program_model = pickle.load(f)
        program_classes = list(program_model.domain.class_var.values)
        logger.info("✓ Program model loaded")
    except Exception as e:
        logger.error(f"✗ Failed to load program model: {e}")
        raise

    try:
        with open(BASE_DIR / "Neural_network_intensity_model_MSPR.pkcls", "rb") as f:
            intensity_model = pickle.load(f)
        intensity_classes = list(intensity_model.domain.class_var.values)
        logger.info("✓ Intensity model loaded")
    except Exception as e:
        logger.error(f"✗ Failed to load intensity model: {e}")
        raise


# ============================================================================
# MODÈLES PYDANTIC
# ============================================================================

class WorkoutInput(BaseModel):
    """Schéma d'entrée pour l'API de prédiction."""
    age: int
    gender: Literal["Male", "Female"]
    height_cm: float
    weight_kg: float
    bmi: float
    body_fat_percentage: float
    resting_bpm: int
    primary_goal: Literal["endurance", "fat_loss", "general_health", "muscle_gain"]
    target_timeline_weeks: int
    fitness_level: Literal["beginner", "intermediate", "advanced"]
    avg_session_duration_min: int
    recent_fatigue_score: float
    has_gym_access: bool
    home_equipment: Literal["none", "dumbbells", "resistance_bands", "barbell", "full_home_gym"]
    available_space_m2: float
    available_days_per_week: int
    preferred_session_duration_min: int
    preferred_activities: str
    preferred_time_of_day: Literal["morning", "afternoon", "evening"]
    workout_variety_preference: float
    injury_type: Literal["none", "ankle", "knee", "back", "shoulder", "wrist"]
    injury_severity: Literal["none", "mild", "moderate", "severe"]
    medical_condition: Literal["none", "diabetes", "hypertension", "asthma", "cardiac"]
    fatigue_level: float

    @field_validator("age", "resting_bpm", "target_timeline_weeks", "avg_session_duration_min", 
                     "available_days_per_week", "preferred_session_duration_min", mode="before")
    @classmethod
    def validate_positive_int(cls, v):
        if v is None:
            raise ValueError("Valeur ne peut pas être null")
        if isinstance(v, (int, float)) and v <= 0:
            raise ValueError("Doit être > 0")
        return v

    @field_validator("height_cm", "weight_kg", "bmi", "body_fat_percentage", "recent_fatigue_score",
                     "available_space_m2", "preferred_session_duration_min", "workout_variety_preference",
                     "fatigue_level", mode="before")
    @classmethod
    def validate_positive_float(cls, v):
        if v is None:
            raise ValueError("Valeur ne peut pas être null")
        try:
            val = float(v)
            if val <= 0:
                raise ValueError("Doit être > 0")
            return val
        except (ValueError, TypeError):
            raise ValueError("Doit être un nombre > 0")


class PredictionResponse(BaseModel):
    """Schéma de réponse de l'API."""
    recommended_program: str
    recommended_intensity: str


# ============================================================================
# TRANSFORMATIONS DE DONNÉES
# ============================================================================

def parse_preferred_activities(activities_str: str) -> list:
    """Parser la string d'activités en liste."""
    if not activities_str:
        return []
    return [a.strip().lower() for a in activities_str.replace("|", ",").split(",") if a.strip()]


def create_feature_vector(data: WorkoutInput) -> Table:
    """
    Transformer les données brutes en Orange Table avec les 54 features one-hot encodées.
    Orange appliquera automatiquement la normalisation définie dans le domaine du modèle.
    """
    
    # Créer dictionnaire avec tous les noms de features
    feature_dict = {}
    
    # Features numériques (14)
    feature_dict["age"] = float(data.age)
    feature_dict["height_cm"] = float(data.height_cm)
    feature_dict["weight_kg"] = float(data.weight_kg)
    feature_dict["bmi"] = float(data.bmi)
    feature_dict["body_fat_percentage"] = float(data.body_fat_percentage)
    feature_dict["resting_bpm"] = float(data.resting_bpm)
    feature_dict["target_timeline_weeks"] = float(data.target_timeline_weeks)
    feature_dict["avg_session_duration_min"] = float(data.avg_session_duration_min)
    feature_dict["recent_fatigue_score"] = float(data.recent_fatigue_score)
    feature_dict["available_space_m2"] = float(data.available_space_m2)
    feature_dict["available_days_per_week"] = float(data.available_days_per_week)
    feature_dict["preferred_session_duration_min"] = float(data.preferred_session_duration_min)
    feature_dict["workout_variety_preference"] = float(data.workout_variety_preference)
    feature_dict["fatigue_level"] = float(data.fatigue_level)

    # Features catégorielles encodées (one-hot)
    feature_dict["gender=Female"] = 1.0 if data.gender == "Female" else 0.0
    feature_dict["gender=Male"] = 1.0 if data.gender == "Male" else 0.0

    for goal in ["endurance", "fat_loss", "general_health", "muscle_gain"]:
        feature_dict[f"primary_goal={goal}"] = 1.0 if data.primary_goal == goal else 0.0

    for level in ["advanced", "beginner", "intermediate"]:
        feature_dict[f"fitness_level={level}"] = 1.0 if data.fitness_level == level else 0.0

    feature_dict["has_gym_access=False"] = 1.0 if not data.has_gym_access else 0.0
    feature_dict["has_gym_access=True"] = 1.0 if data.has_gym_access else 0.0

    for equipment in ["barbell", "dumbbells", "full_home_gym", "none", "resistance_bands"]:
        feature_dict[f"home_equipment={equipment}"] = 1.0 if data.home_equipment == equipment else 0.0

    activities = set(parse_preferred_activities(data.preferred_activities))
    for activity in ["cardio", "hiit", "outdoor", "sport", "strength", "yoga"]:
        feature_dict[f"preferred_activities={activity}"] = 1.0 if activity in activities else 0.0

    for time in ["afternoon", "evening", "morning"]:
        feature_dict[f"preferred_time_of_day={time}"] = 1.0 if data.preferred_time_of_day == time else 0.0

    for injury in ["ankle", "back", "knee", "none", "shoulder", "wrist"]:
        feature_dict[f"injury_type={injury}"] = 1.0 if data.injury_type == injury else 0.0

    for severity in ["mild", "moderate", "none", "severe"]:
        feature_dict[f"injury_severity={severity}"] = 1.0 if data.injury_severity == severity else 0.0

    for condition in ["asthma", "cardiac", "diabetes", "hypertension", "none"]:
        feature_dict[f"medical_condition={condition}"] = 1.0 if data.medical_condition == condition else 0.0

    # Construire array en respectant EXACTEMENT l'ordre des attributs du domaine
    # program_model.domain.attributes est un tuple d'objets Attribute
    try:
        attrs = program_model.domain.attributes
        attr_names = [attr.name for attr in attrs]
        logger.info(f"Domain has {len(attr_names)} attributes")
        
        # Construire le vecteur de features dans le même ordre
        feature_values = [feature_dict.get(name, 0.0) for name in attr_names]
        feature_array = np.array([feature_values], dtype=np.float32)
        
        logger.info(f"Feature array shape: {feature_array.shape}")
        
        # Ajouter une colonne pour la classe cible (peut être 0 puisque c'est une prédiction)
        class_array = np.array([[0]], dtype=np.float32)
        X = np.hstack([feature_array, class_array])
        
        logger.info(f"Final array shape (with class): {X.shape}")
        
        # Créer Orange Table (appliquera normalisation automatiquement)
        table = Table.from_numpy(program_model.domain, X)
        logger.info(f"Table created: {table.X.shape}")
        return table
    except Exception as e:
        logger.error(f"Error creating feature vector: {type(e).__name__}: {e}")
        logger.error(f"Domain attributes type: {type(program_model.domain.attributes)}")
        raise


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Charger les modèles au démarrage."""
    load_models()


@app.get("/health")
async def health():
    """Vérifier la santé du service."""
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: WorkoutInput):
    """
    Prédire le programme d'entraînement et l'intensité.
    
    Les données d'entrée sont validées (non-null, sans NaN).
    Retourne les prédictions des deux modèles de réseau de neurones.
    """
    try:
        # Transformer les données en Orange Table normalisée
        feature_table = create_feature_vector(input_data)
        
        # Prédictions (retournent les indices des classes)
        program_pred = program_model(feature_table)
        intensity_pred = intensity_model(feature_table)
        
        # Extraire les indices
        program_idx = int(program_pred[0])
        intensity_idx = int(intensity_pred[0])
        
        # Mapper les indices aux noms de classe
        program_name = program_classes[program_idx]
        intensity_name = intensity_classes[intensity_idx]
        
        logger.info(f"Prediction: program={program_idx}({program_name}), intensity={intensity_idx}({intensity_name})")
        
        return PredictionResponse(
            recommended_program=program_name,
            recommended_intensity=intensity_name
        )
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la prédiction")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
