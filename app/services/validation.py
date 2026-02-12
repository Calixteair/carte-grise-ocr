import re
from typing import Optional, Dict

class CarPlateValidator:
    def __init__(self):
        # Common regex patterns for validation
        self.patterns = {
            "FR_NUM_IMMATRICULATION_NEW": r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", # AB-123-CD
            "FR_NUM_IMMATRICULATION_OLD": r"^\d{1,4}\s[A-Z]{2}\s\d{2}$", # 1234 AB 56
            "TN_NUM_IMMATRICULATION": r"^\d{1,3}\sTUN\s\d{1,4}$", # 123 TUN 4567
            "DATE": r"^\d{4}-\d{2}-\d{2}$", # YYYY-MM-DD
            "EMAIL": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "VIN": r"^[A-HJ-NPR-Z0-9]{17}$", # Standard VIN format
            "POWER": r"^\d+(\.\d+)?$", # Numeric value for power/fiscal
        }

    def validate_field(self, field_name: str, value: Optional[str], country_code: str = "FR") -> bool:
        if value is None:
            return True # Allow None values, schema handles optionality

        if field_name == "numero_immatriculation":
            if country_code == "FR":
                return re.match(self.patterns["FR_NUM_IMMATRICULATION_NEW"], value) is not None or \
                       re.match(self.patterns["FR_NUM_IMMATRICULATION_OLD"], value) is not None
            elif country_code == "TN":
                return re.match(self.patterns["TN_NUM_IMMATRICULATION"], value) is not None
        elif "date" in field_name:
            return re.match(self.patterns["DATE"], value) is not None
        elif field_name == "numero_identification": # VIN for FR
            return re.match(self.patterns["VIN"], value) is not None
        elif field_name == "numero_serie": # VIN for TN
            return re.match(self.patterns["VIN"], value) is not None
        elif "puissance" in field_name or "cylindree" in field_name or "masse" in field_name or \
             "ptac" in field_name or "poids" in field_name or "charge_utile" in field_name or \
             "co2" in field_name or "nombre_places" in field_name:
            return re.match(self.patterns["POWER"], value) is not None

        return True # If no specific pattern, consider valid

    def validate_car_plate_data(self, data: Dict, country_code: str = "FR") -> Dict:
        """
        Validates a dictionary of extracted car plate data against known patterns.
        Returns a dictionary with validation results for each field.
        """
        validation_results = {}
        for field, value in data.items():
            is_valid = self.validate_field(field, str(value) if value is not None else None, country_code)
            validation_results[field] = {
                "value": value,
                "is_valid": is_valid,
                "message": "Valid" if is_valid else "Invalid format"
            }
        return validation_results

car_plate_validator = CarPlateValidator()
