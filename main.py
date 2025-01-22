from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from models import GenerateRequest, GenerateResponse, HistoryItem

app = FastAPI(
    title="Roams Back-end IA",
    description="API que genera texto usando un modelo preentrenado de HuggingFace",
    version="1.0.0",
)

security = HTTPBearer()
API_TOKEN = "roams-token"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Esquema de autenticación inválido")
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido o no proveído")
    return True


MODEL_NAME = "gpt2"

print("Descargando modelo. Esto podría tardar un poco la primera vez...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()
print("Modelo GPT2 descargado y cargado en memoria.")

history_data = []

@app.post("/generate", response_model=GenerateResponse, summary="Generar texto con GPT-2")
def generate_text(
    request: GenerateRequest,
    # Descomenta la siguiente línea si quieres habilitar el token de seguridad
    # authorized: bool = Depends(verify_token)
):

    if not request.prompt.strip():
        raise HTTPException(
            status_code=422, detail="El prompt no puede estar vacío."
        )
    input_ids = tokenizer.encode(request.prompt, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=input_ids,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    item = HistoryItem(
        prompt=request.prompt,
        generated_text=generated_text,
        parameters=request.dict(exclude={"prompt"})
    )
    history_data.append(item)

    return GenerateResponse(
        generated_text=generated_text,
        prompt=request.prompt,
        used_parameters=request.dict(exclude={"prompt"})
    )

@app.get("/history", response_model=List[HistoryItem], summary="Obtener histórico de textos generados")
def get_history(
    # authorized: bool = Depends(verify_token)
):
    return history_data
