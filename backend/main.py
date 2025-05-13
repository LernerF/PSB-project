from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_service import chat_service
import uuid

app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str
    user_id: str

@app.post("/api/send_message")
async def send_message(message: Message, request: Request):
    # Проверка спама
    if chat_service.check_spam(message.user_id):
        raise HTTPException(status_code=429, detail="Слишком много запросов. Пожалуйста, подождите.")
    
    # Получение ответа от RAG системы
    response_text = await chat_service.get_rag_response(message.text)
    
    # Логирование вопроса и ответа
    await chat_service.log_message(message.user_id, message.text, response_text)
    
    return {"text": response_text}

@app.get("/api/init_chat", response_model=dict)
async def init_chat():
    # Генерация уникального ID для пользователя
    return {"user_id": str(uuid.uuid4())}

# Монтируем статические файлы Vue приложения
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)