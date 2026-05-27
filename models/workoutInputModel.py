from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import Literal

class WorkoutInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "age": 30,
                    "gender": "Male",
                    "height_cm": 180.0,
                    "weight_kg": 75.0,
                    "bmi": 23.1,
                    "body_fat_percentage": 15.0,
                    "resting_bpm": 65,
                    "health_goal": "muscle_gain",
                    "target_timeline_weeks": 12,
                    "fitness_level": "intermediate",
                    "fatigue_score": 5.0,
                    "has_gym_access": True,
                    "workout_variety_preference": 6.0,
                    "injury_type": "none",
                    "injury_severity": "none",
                    "medical_condition": "none",
                }
            ]
        }
    )

    age: int = Field(..., description="Âge en années", examples=[30])
    gender: Literal["Male", "Female"] = Field(..., description="Genre", examples=["Male"])
    height_cm: float = Field(..., description="Taille en centimètres", examples=[180.0])
    weight_kg: float = Field(..., description="Poids en kilogrammes", examples=[75.0])
    bmi: float = Field(..., description="Indice de masse corporelle", examples=[23.1])
    body_fat_percentage: float = Field(..., description="Pourcentage de masse grasse", examples=[15.0])
    resting_bpm: int = Field(..., description="Fréquence cardiaque au repos", examples=[65])
    health_goal: Literal["endurance", "fat_loss", "general_health", "muscle_gain"] = Field(
        ..., description="Objectif principal", examples=["muscle_gain"]
    )
    target_timeline_weeks: int = Field(..., description="Durée objectif en semaines", examples=[12])
    fitness_level: Literal["beginner", "intermediate", "advanced"] = Field(
        ..., description="Niveau de forme", examples=["intermediate"]
    )
    fatigue_score: float = Field(..., description="Score de fatigue récent (0-10)", examples=[5.0])
    has_gym_access: bool = Field(..., description="Accès à une salle de sport", examples=[True])
    workout_variety_preference: float = Field(
        ..., description="Préférence de variété (0-10)", examples=[6.0]
    )
    injury_type: Literal["none", "ankle", "knee", "back", "shoulder", "wrist"] = Field(
        ..., description="Type de blessure", examples=["none"]
    )
    injury_severity: Literal["none", "mild", "moderate", "severe"] = Field(
        ..., description="Gravité de la blessure", examples=["none"]
    )
    medical_condition: Literal["none", "diabetes", "hypertension", "asthma", "cardiac"] = Field(
        ..., description="Condition médicale", examples=["none"]
    )

    @field_validator("age", "resting_bpm", "target_timeline_weeks", mode="before")
    @classmethod
    def validate_positive_int(cls, v):
        if v is None:
            raise ValueError("Valeur ne peut pas être null")
        if isinstance(v, (int, float)) and v <= 0:
            raise ValueError("Doit être > 0")
        return v

    @field_validator("height_cm", "weight_kg", "bmi", "body_fat_percentage", "fatigue_score",
                     "workout_variety_preference", mode="before")
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

    @field_validator("body_fat_percentage")
    @classmethod
    def validate_body_fat(cls, v):
        if v < 5 or v > 100:
            raise ValueError("body_fat_percentage doit être entre 5 et 100")
        return v

    @field_validator("workout_variety_preference")
    @classmethod
    def validate_workout_variety(cls, v):
        if v < 0 or v > 10:
            raise ValueError("workout_variety_preference doit être entre 0 et 10")
        return v

    @field_validator("fatigue_score")
    @classmethod
    def validate_fatigue(cls, v):
        if v < 0 or v > 10:
            raise ValueError("fatigue_score doit être entre 0 et 10")
        return v

    @field_validator("resting_bpm")
    @classmethod
    def validate_bpm(cls, v):
        if v < 30 or v > 150:
            raise ValueError("resting_bpm doit être entre 30 et 150")
        return v