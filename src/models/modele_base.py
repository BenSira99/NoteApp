"""
Module contenant la classe de base pour tous les modèles de données.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ModeleBase(BaseModel):
    """
    Classe de base fournissant les champs communs et la configuration.
    """
    model_config = ConfigDict(from_attributes=True)

    identifiant: Optional[int] = Field(default=None, alias="id")
    date_creation: datetime = Field(default_factory=datetime.now)
    date_modification: datetime = Field(default_factory=datetime.now)

    def actualiser_date_modification(self) -> None:
        """
        Met à jour la date de modification à l'instant présent.
        """
        self.date_modification = datetime.now()
