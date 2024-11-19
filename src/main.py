import os
import json
import logging
from typing import List, Type
from mlp_sdk.abstract import Task
from mlp_sdk.hosting.host import host_mlp_cloud
import requests
from pydantic import BaseModel

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RephraseInput(BaseModel):
    text: str

class RephraseOutput(BaseModel):
    rephrased_texts: List[str] = []

class RephraseTask(Task):

    def __init__(self, params=None, service_sdk=None) -> None:
        super().__init__(params, service_sdk)
        self.api_token = 'your_api_token'  
        self.account_id = 'your_account_id'  
        self.url = "https://caila.io/api/mlpgate/account/just-ai/model/openai-proxy/predict"
        logger.debug("Инициализация завершена")

    @property
    def predict_input_schema(self) -> Type[BaseModel]:
        return RephraseInput

    @property
    def predict_output_schema(self) -> Type[BaseModel]:
        return RephraseOutput

    def predict(self, data: RephraseInput, config: BaseModel) -> RephraseOutput:
        text_to_rephrase = data.text
        logger.debug(f"Получен текст для перефразирования: {text_to_rephrase}")
        if not text_to_rephrase:
            logger.debug("Пустой текст. Возвращается пустой список.")
            return RephraseOutput(rephrased_texts=[])

        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "MLP-API-KEY": self.api_token
        }

        payload = {
            "chat": {
                "model": "gpt-4o-mini",  
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that rephrases text. Provide only the rephrased versions without any numbering, additional text, or explanations. Each rephrased version should be on a new line."
                    },
                    {
                        "role": "user",
                        "content": f"Rephrase the following text in 10 different ways:\n{text_to_rephrase}"
                    }
                ]
            }
        }

        logger.debug(f"Сформирован запрос: {json.dumps(payload, indent=2, ensure_ascii=False)}")

        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Получен ответ от модели: {json.dumps(result, indent=2, ensure_ascii=False)}")

            if 'chat' in result and 'choices' in result['chat']:
                rephrased_text = result['chat']['choices'][0]['message']['content'].strip()
                # Разбиваем ответ на отдельные строки и формируем список
                rephrased_texts = [line.strip() for line in rephrased_text.split('\n') if line.strip()]
                logger.debug(f"Перефразированный текст: {rephrased_texts}")
                return RephraseOutput(rephrased_texts=rephrased_texts)
            else:
                logger.error(f"Неожиданная структура ответа: {result}")
                return RephraseOutput(rephrased_texts=[])

        except requests.exceptions.RequestException as e:
            logger.exception(f"Ошибка во время запроса: {e}")
            return RephraseOutput(rephrased_texts=[])


    @property
    def init_config_schema(self) -> Type[BaseModel]:
        return BaseModel

if __name__ == "__main__":
    host_mlp_cloud(RephraseTask, params=None)
