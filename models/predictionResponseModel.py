from pydantic import BaseModel

class PredictionResponse(BaseModel):
    recommended_program: str
    recommended_intensity: str
    recommended_plan: list