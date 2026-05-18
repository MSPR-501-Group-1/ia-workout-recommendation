from pydantic import BaseModel, field_validator
from typing import Literal

class WorkoutInput(BaseModel):
    age: int
    gender: Literal["Male", "Female"]
    height_cm: float
    weight_kg: float
    bmi: float
    body_fat_percentage: float
    resting_bpm: int
    health_goal: Literal["endurance", "fat_loss", "general_health", "muscle_gain"]
    target_timeline_weeks: int
    fitness_level: Literal["beginner", "intermediate", "advanced"]
    fatigue_score: float
    has_gym_access: bool
    workout_variety_preference: float
    injury_type: Literal["none", "ankle", "knee", "back", "shoulder", "wrist"]
    injury_severity: Literal["none", "mild", "moderate", "severe"]
    medical_condition: Literal["none", "diabetes", "hypertension", "asthma", "cardiac"]

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