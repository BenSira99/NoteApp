"""
Modèle ParametreApplication - Stockage des préférences et de la configuration de l'application.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session
from .base_de_donnees import Base

class ParametreApplication(Base):
    """
    Modèle pour stocker les paramètres sous forme de paires clé-valeur.
    """
    __tablename__ = 'parametres_application'

    cle = Column(String(255), primary_key=True)
    valeur = Column(String, nullable=True)
    date_mise_a_jour = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f"<ParametreApplication(cle='{self.cle}', valeur='{self.valeur}')>"

    @staticmethod
    def obtenir_valeur(session: Session, cle: str, defaut=None):
        """
        Récupère la valeur d'un paramètre par sa clé.
        """
        parametre = session.query(ParametreApplication).filter(ParametreApplication.cle == cle).first()
        if parametre:
            return parametre.valeur
        return defaut

    @staticmethod
    def definir_valeur(session: Session, cle: str, valeur) -> None:
        """
        Définit ou met à jour la valeur d'un paramètre.
        """
        parametre = session.query(ParametreApplication).filter(ParametreApplication.cle == cle).first()
        if parametre:
            parametre.valeur = str(valeur)
        else:
            parametre = ParametreApplication(cle=cle, valeur=str(valeur))
            session.add(parametre)
        session.commit()
