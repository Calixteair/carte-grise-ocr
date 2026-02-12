from app.core.celery_app import celery_app
from app.database import SessionLocal
from app.models.document import Document
from app.services.ai.mistral_client import mistral_client
from app.services.ai.prompts import COUNTRY_PROMPTS
from app.services.image_processing import preprocess_image
from app.services.validation import car_plate_validator

@celery_app.task(name="process_image_for_extraction")
def process_image_for_extraction(document_id: int, image_base64: str, country_code: str):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            # Log error or handle missing document
            return {"status": "failed", "message": f"Document with ID {document_id} not found."}

        # 1. Pre-process image
        try:
            processed_image_base64 = preprocess_image(image_base64.encode('utf-8'))
        except Exception as e:
            document.status = "failed"
            document.extracted_data = {"error": f"Image preprocessing failed: {str(e)}"}
            db.commit()
            return {"status": "failed", "message": f"Image preprocessing failed: {str(e)}"}

        # 2. Get AI prompt based on country
        prompt = COUNTRY_PROMPTS.get(country_code)
        if not prompt:
            document.status = "failed"
            document.extracted_data = {"error": f"No prompt found for country code: {country_code}"}
            db.commit()
            return {"status": "failed", "message": f"No prompt found for country code: {country_code}"}

        # 3. Call Mistral AI for extraction
        try:
            extracted_data = mistral_client.extract_car_plate_data(processed_image_base64, prompt)
        except Exception as e:
            document.status = "failed"
            document.extracted_data = {"error": f"AI extraction failed: {str(e)}"}
            db.commit()
            return {"status": "failed", "message": f"AI extraction failed: {str(e)}"}

        # 4. Validate extracted data
        validation_results = car_plate_validator.validate_car_plate_data(extracted_data, country_code)

        document.extracted_data = {
            "raw_extraction": extracted_data,
            "validation_results": validation_results
        }
        document.status = "completed"
        db.commit()
        return {"status": "completed", "document_id": document.id}
    except Exception as e:
        if document:
            document.status = "failed"
            document.extracted_data = {"error": f"An unexpected error occurred: {str(e)}"}
            db.commit()
        return {"status": "failed", "message": f"An unexpected error occurred: {str(e)}"}
    finally:
        db.close()
