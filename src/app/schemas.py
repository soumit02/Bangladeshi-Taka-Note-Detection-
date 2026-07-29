from pydantic import BaseModel

# Schema for the API output response
class PredictionResponse(BaseModel):
    class_name: str
    confidence: float
    source: str
    processed_by: str