from typing import Optional
from pydantic import BaseModel, Field

class CarPlateTN(BaseModel):
    # Numéro d'immatriculation (Matricule)
    numero_immatriculation: Optional[str] = Field(None, description="Numéro d'immatriculation (Matricule)")
    # Date de première mise en circulation (Date de 1ère MC)
    date_premiere_mise_en_circulation: Optional[str] = Field(None, description="Date de 1ère MC")
    # Propriétaire (Nom et Prénom ou Raison Sociale)
    proprietaire: Optional[str] = Field(None, description="Nom et Prénom ou Raison Sociale du Propriétaire")
    # Adresse du Propriétaire
    adresse_proprietaire: Optional[str] = Field(None, description="Adresse du Propriétaire")
    # Marque du véhicule
    marque: Optional[str] = Field(None, description="Marque du véhicule")
    # Type du véhicule
    type_vehicule: Optional[str] = Field(None, description="Type du véhicule")
    # Numéro de série dans la série du type (VIN)
    numero_serie: Optional[str] = Field(None, description="Numéro de série dans la série du type (VIN)")
    # Puissance fiscale (CV)
    puissance_fiscale: Optional[str] = Field(None, description="Puissance fiscale (CV)")
    # Carburant
    carburant: Optional[str] = Field(None, description="Carburant")
    # Nombre de places assises
    nombre_places: Optional[str] = Field(None, description="Nombre de places assises")
    # Poids Total Autorisé en Charge (PTAC)
    ptac: Optional[str] = Field(None, description="Poids Total Autorisé en Charge (PTAC)")
    # Poids à Vide
    poids_vide: Optional[str] = Field(None, description="Poids à Vide")
    # Charge Utile
    charge_utile: Optional[str] = Field(None, description="Charge Utile")
    # Genre
    genre: Optional[str] = Field(None, description="Genre")
    # Usage
    usage: Optional[str] = Field(None, description="Usage")
    # Couleur
    couleur: Optional[str] = Field(None, description="Couleur")
    # Numéro du moteur
    numero_moteur: Optional[str] = Field(None, description="Numéro du moteur")
    # Date de délivrance de la carte grise
    date_delivrance: Optional[str] = Field(None, description="Date de délivrance de la carte grise")
