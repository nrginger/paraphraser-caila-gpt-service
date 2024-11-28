import os
import json
import logging
from typing import List, Type
from mlp_sdk.abstract import Task
from mlp_sdk.hosting.host import host_mlp_cloud
import requests
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RephraseInput(BaseModel):
    texts: str

class RephraseOutput(BaseModel):
    texts_list: List[dict] = []

class RephraseConfig(BaseModel):
    batch_size: int
    diversity: float

class RephraseTask(Task):

    def __init__(self, params=None, service_sdk=None) -> None:
        super().__init__(params, service_sdk)
        self.api_token = 'your_api_token'  # insert your API token
        self.account_id = 'your_account_id'  # insert your account ID
        self.url = "https://caila.io/api/mlpgate/account/just-ai/model/openai-proxy/predict"
        logger.debug("Инициализация завершена")

    @property
    def predict_input_schema(self) -> Type[BaseModel]:
        return RephraseInput

    @property
    def predict_output_schema(self) -> Type[BaseModel]:
        return RephraseOutput

    @property
    def init_config_schema(self) -> Type[BaseModel]:
        return RephraseConfig

    def predict(self, data: RephraseInput, config: RephraseConfig) -> RephraseOutput:
        texts_to_rephrase = data.texts
        logger.debug(f"Получен текст для перефразирования: {texts_to_rephrase}")
        if not texts_to_rephrase:
            logger.debug("Пустой текст. Возвращается пустой список.")
            return RephraseOutput(rephrased_texts=[])

        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "MLP-API-KEY": self.api_token
        }

        payload = {
            "chat": {
                "model": "gpt-4o-mini", #choose any available model
                "temperature": config.diversity,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that rephrases text. Provide only the rephrased versions without any numbering, additional text, or explanations. Each rephrased version should be on a new line."
                    },
                    {
                        "role": "user",
                        "content": f"Rephrase the following text or texts in {config.batch_size} different ways:\n{texts_to_rephrase}"
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
                rephrased_texts = result['chat']['choices'][0]['message']['content'].strip()
                rephrased_values = [line.strip() for line in rephrased_texts.split('\n') if line.strip()]
                output_dict = {
                    "values": rephrased_values
                    }
                logger.debug(f"Перефразированный текст: {output_dict}")
                return RephraseOutput(texts_list=[output_dict])
            else:
                logger.error(f"Неожиданная структура ответа: {result}")
                return RephraseOutput(texts_list=[])

        except requests.exceptions.RequestException as e:
            logger.exception(f"Ошибка во время запроса: {e}")
            return RephraseOutput(texts_list=[])


    @property
    def init_config_schema(self) -> Type[BaseModel]:
        return BaseModel

if __name__ == "__main__":
    host_mlp_cloud(RephraseTask, params=None)
