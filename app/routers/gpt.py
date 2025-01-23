from fastapi import HTTPException, APIRouter, Depends
from db.connection import conn
from middlewares.auth import verify_token
from typing import List
from gpt_model import GPTModel
from models.request_response import GenerateRequest, GenerateResponse, HistoryItem
import json

router = APIRouter()
gpt_model = GPTModel("gpt2")
cursor = conn.cursor()

@router.post("/generate", response_model=GenerateResponse, summary="Generar texto con GPT-2")
def generate_text(
    request: GenerateRequest,
    username: str = Depends(verify_token)
):
    if not request.prompt.strip():
        raise HTTPException(status_code=422, detail="El prompt no puede estar vacío.")

    generated_text = gpt_model.generate_text(
        prompt=request.prompt,
        max_length=request.max_length,
        temperature=request.temperature,
        top_p=request.top_p
    )

    parameters_json = json.dumps(request.model_dump(exclude={"prompt"}))
    cursor.execute("""
        INSERT INTO history (username, prompt, generated_text, parameters)
        VALUES (?, ?, ?, ?)
    """, (username, request.prompt, generated_text, parameters_json))
    conn.commit()

    return GenerateResponse(
        generated_text=generated_text,
        prompt=request.prompt,
        used_parameters=request.model_dump(exclude={"prompt"})
    )

@router.get("/history", response_model=List[HistoryItem], summary="Obtener histórico de textos generados")
def get_history(
    username: str = Depends(verify_token)
):
    cursor.execute("""
        SELECT prompt, generated_text, parameters
        FROM history
        WHERE username=?
        ORDER BY created_at DESC
    """, (username,))
    rows = cursor.fetchall()

    history_items = []
    for row in rows:
        history_items.append(HistoryItem(
            prompt=row[0],
            generated_text=row[1],
            parameters=json.loads(row[2]) if row[2] else {}
        ))
    return history_items