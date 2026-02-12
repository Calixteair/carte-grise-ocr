import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from app.core.config import settings
from app.schemas.car_plate_fr import CarPlateFR
from app.schemas.car_plate_tn import CarPlateTN

class MistralAIClient:
    def __init__(self):
        self.client = MistralClient(api_key=settings.MISTRAL_API_KEY)

    def extract_car_plate_data(self, image_base64: str, country_prompt: str) -> dict:
        messages = [
            ChatMessage(
                role="user",
                content=[
                    {"type": "text", "text": country_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
                ]
            )
        ]

        # Use the JSON mode for the response
        chat_response = self.client.chat(
            model="mistral-large-latest", # Or another appropriate model
            messages=messages,
            response_format={"type": "json_object"}
        )

        response_content = chat_response.choices[0].message.content
        return json.loads(response_content)

mistral_client = MistralAIClient()
