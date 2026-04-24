"""
Modèle de catégorie pour organiser les notes.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base_de_donnees import Base

class Categorie(Base):
    """
    Modèle représentant une catégorie de notes.
    """
    __tablename__ = "categories"

    identifiant = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    couleur = Column(String(7), default="#58A6FF")  # Couleur Hex
    icone = Column(String(50), default="folder")
    date_creation = Column(DateTime, default=datetime.now)

    # Relations
    notes = relationship("Note", back_populates="categorie", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return self.nom

    @staticmethod
    def obtenir_categories_par_defaut() -> list:
        """
        Retourne une liste de catégories par défaut.
        """
        return [
            {"nom": "Personnel", "couleur": "#6200EE", "icone": "person"},
            {"nom": "Travail", "couleur": "#03DAC6", "icone": "work"},
            {"nom": "Idées", "couleur": "#FFC107", "icone": "lightbulb"},
            {"nom": "Courses", "couleur": "#4CAF50", "icone": "shopping_cart"},
        ]

    @classmethod
    def creer_par_defaut(cls, session) -> None:
        """
        Crée les catégories par défaut si aucune n'existe.
        """
        if session.query(cls).count() == 0:
            for donnees in cls.obtenir_categories_par_defaut():
                categorie = cls(**donnees)
                session.add(categorie)
            session.commit()
