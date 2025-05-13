import time
from datetime import datetime
from typing import List, Dict
import aiofiles
import json
import os
from typing import Dict, Any, Optional
import requests

class ChatService:
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.user_last_request = {}
        self.spam_threshold = 3  # секунд между сообщениями
        self.log_file = "chat_logs.json"
        
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    async def log_message(self, user_id: str, message: str, response: str):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "question": message,
            "answer": response
        }
        
        try:
            async with aiofiles.open(self.log_file, mode='a') as f:
                await f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error logging message: {e}")

    def check_spam(self, user_id: str) -> bool:
        current_time = time.time()
        last_request = self.user_last_request.get(user_id, 0)
        
        if current_time - last_request < self.spam_threshold:
            return True
            
        self.user_last_request[user_id] = current_time
        return False

    async def get_rag_response(self, question: str, context: Optional[str] = None, 
              max_tokens: int = 150, temperature: float = 0.7) -> str:
        # Здесь должна быть интеграция с вашим RAG API
        # Это примерная реализация - замените на реальный вызов API

        """
        Отправка запроса к RAG API
        
        :param question: Вопрос или промпт
        :param context: Контекст для поиска (опционально)
        :param max_tokens: Максимальное количество токенов в ответе
        :param temperature: Параметр температуры для генерации
        :return: Ответ от API в виде словаря
        """
        endpoint = f"{self.api_url}/query"
        payload = {
            "question": question,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if context:
            payload["context"] = context
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к RAG API: {e}")
            return {"error": str(e)}
        # try:
        #     # Пример: response = await rag_api_call(question)
        #     # return response["answer"]
            
        #     # Заглушка для демонстрации
        #     return f"Ответ на вопрос: '{question}'. Это демо-ответ от RAG системы."
        # except Exception as e:
        #     print(f"Error calling RAG API: {e}")
        #     return "Извините, не удалось получить ответ от системы."

chat_service = ChatService(api_url="https://api.rag.shawel.ru/api/v1")