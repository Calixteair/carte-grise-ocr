from app.schemas.car_plate_fr import CarPlateFR
from app.schemas.car_plate_tn import CarPlateTN

PROMPT_FR = f"""
You are an expert in French car registration documents (cartes grises).
Your task is to extract specific fields from the provided image of a French carte grise.
Return the extracted information as a JSON object, strictly following the Pydantic schema for CarPlateFR.
If a field is not found or is not applicable, set its value to null.

Here is the Pydantic schema you must follow:
{CarPlateFR.model_json_schema()}

Ensure the JSON output is perfectly valid and directly parsable.
"""

PROMPT_TN = f"""
You are an expert in Tunisian car registration documents (cartes grises).
Your task is to extract specific fields from the provided image of a Tunisian carte grise.
Return the extracted information as a JSON object, strictly following the Pydantic schema for CarPlateTN.
If a field is not found or is not applicable, set its value to null.

Here is the Pydantic schema you must follow:
{CarPlateTN.model_json_schema()}

Ensure the JSON output is perfectly valid and directly parsable.
"""

# Dictionary to easily access prompts by country code
COUNTRY_PROMPTS = {
    "FR": PROMPT_FR,
    "TN": PROMPT_TN,
}
