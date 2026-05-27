from pydantic import BaseModel, Field


class PlanItem(BaseModel):
    exercise: str = Field(..., description="Nom de l'exercice")
    muscle_group: str = Field(..., description="Groupe musculaire ciblé")
    equipment: str = Field(..., description="Équipement requis")
    reps: int = Field(..., description="Nombre de répétitions")
    series: int = Field(..., description="Nombre de séries")
    repos: int = Field(..., description="Temps de repos (secondes)")

class PredictionResponse(BaseModel):
    recommended_program: str = Field(..., description="Programme d'entraînement recommandé")
    recommended_intensity: str = Field(..., description="Intensité recommandée")
    recommended_plan: list[PlanItem] = Field(..., description="Plan d'exercices recommandé")