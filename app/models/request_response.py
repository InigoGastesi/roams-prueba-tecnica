from typing import Optional, List
from pydantic import BaseModel, Field
class GenerateRequest(BaseModel):
    prompt: str = Field(..., example="Había una vez en un reino muy lejano")
    max_length: Optional[int] = Field(50, example=100, description="Longitud máxima de la respuesta")
    temperature: Optional[float] = Field(1.0, example=0.7, description="Controla la creatividad (0 a 1, etc.)")
    top_p: Optional[float] = Field(0.9, example=0.9, description="Controla la variedad de palabras (0 a 1)")

class GenerateResponse(BaseModel):
    generated_text: str
    prompt: str
    used_parameters: dict


class HistoryItem(BaseModel):
    prompt: str
    generated_text: str
    parameters: dict