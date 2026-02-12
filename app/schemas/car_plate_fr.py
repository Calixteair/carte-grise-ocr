from typing import Optional
from pydantic import BaseModel, Field

class CarPlateFR(BaseModel):
    # Numéro d'immatriculation
    numero_immatriculation: Optional[str] = Field(None, description="A. Numéro d'immatriculation")
    # Date de première immatriculation
    date_premiere_immatriculation: Optional[str] = Field(None, description="B. Date de première immatriculation")
    # Date de première mise en circulation du véhicule (Format YYYY-MM-DD)
    date_mise_en_circulation: Optional[str] = Field(None, description="B. Date de première mise en circulation du véhicule")
    # Nom du titulaire
    nom_titulaire: Optional[str] = Field(None, description="C.1. Nom du titulaire")
    # Prénom du titulaire
    prenom_titulaire: Optional[str] = Field(None, description="C.1. Prénom du titulaire")
    # Adresse du titulaire
    adresse_titulaire: Optional[str] = Field(None, description="C.3. Adresse complète")
    # Marque du véhicule
    marque: Optional[str] = Field(None, description="D.1. Marque")
    # Type, Variante, Version (TVV)
    type_variante_version: Optional[str] = Field(None, description="D.2. Type, Variante, Version (TVV)")
    # Dénomination commerciale
    denomination_commerciale: Optional[str] = Field(None, description="D.3. Dénomination commerciale")
    # Numéro d'identification du véhicule (VIN)
    numero_identification: Optional[str] = Field(None, description="E. Numéro d'identification du véhicule (VIN)")
    # Masse en ordre de marche
    masse_ordre_marche: Optional[str] = Field(None, description="G. Masse en ordre de marche")
    # Puissance fiscale nationale (chevaux fiscaux)
    puissance_fiscale: Optional[str] = Field(None, description="P.6. Puissance fiscale nationale (chevaux fiscaux)")
    # Cylindrée (cm3)
    cylindree: Optional[str] = Field(None, description="P.1. Cylindrée (cm3)")
    # Carburant
    carburant: Optional[str] = Field(None, description="P.3. Carburant")
    # Puissance nette maximale (kW)
    puissance_nette_max: Optional[str] = Field(None, description="P.2. Puissance nette maximale (kW)")
    # Genre national
    genre_national: Optional[str] = Field(None, description="J.1. Genre national")
    # Carrosserie (CE)
    carrosserie_ce: Optional[str] = Field(None, description="J.2. Carrosserie (CE)")
    # Carrosserie (désignation nationale)
    carrosserie_nat: Optional[str] = Field(None, description="J.3. Carrosserie (désignation nationale)")
    # Nombre de places assises
    nombre_places: Optional[str] = Field(None, description="S.1. Nombre de places assises")
    # Poids total autorisé en charge (PTAC)
    ptac: Optional[str] = Field(None, description="F.1. PTAC (Masse en charge maximale techniquement admissible) (kg)")
    # PTAC (masse en charge maximale techniquement admissible) en service dans l’État membre d’immatriculation
    ptac_service: Optional[str] = Field(None, description="F.2. PTAC (masse en charge maximale techniquement admissible) en service dans l’État membre d’immatriculation (kg)")
    # Masse en charge maximale admissible du véhicule en service dans l’État membre d’immatriculation
    masse_max_service: Optional[str] = Field(None, description="F.3. Masse en charge maximale admissible du véhicule en service dans l’État membre d’immatriculation (kg)")
    # CO2 (g/km)
    co2: Optional[str] = Field(None, description="V.7. CO2 (g/km)")
    # Date du certificat d'immatriculation
    date_certificat: Optional[str] = Field(None, description="Z. Date du certificat d'immatriculation")
    # Numéro de formule du certificat
    numero_formule: Optional[str] = Field(None, description="Numéro de formule du certificat (2009-2019)")
    # Numéro de série du certificat
    numero_serie: Optional[str] = Field(None, description="Numéro de série du certificat (depuis 2019)")
