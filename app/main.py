from fastapi import FastAPI, HTTPException, Depends, Body
from routers.user import router as user_router
from routers.gpt import router as gpt_router
app = FastAPI(
    title="Roams Back-end IA",
    description="API que genera texto usando un modelo preentrenado de HuggingFace",
    version="1.0.0",
)


app.include_router(user_router)
app.include_router(gpt_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)