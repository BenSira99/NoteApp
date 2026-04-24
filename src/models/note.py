"""
Modèle Note - entité centrale de l'application de prise de notes.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, or_
from sqlalchemy.orm import relationship, Session
from .base_de_donnees import Base

class Note(Base):
    """
    Modèle Note représentant une entrée unique.
    """
    __tablename__ = "notes"

    identifiant = Column(Integer, primary_key=True)
    titre = Column(String(200), nullable=False)
    contenu = Column(Text, default="")
    id_categorie = Column(Integer, ForeignKey("categories.identifiant", ondelete="SET NULL"), nullable=True)
    est_chiffree = Column(Boolean, default=False)
    est_favoris = Column(Boolean, default=False)
    date_rappel = Column(DateTime, nullable=True)
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relations
    categorie = relationship("Categorie", back_populates="notes")
    pieces_jointes = relationship("PieceJointe", back_populates="note", cascade="all, delete-orphan")

    def __str__(self) -> str:
        return self.titre

    def obtenir_aperçu(self, longueur_max: int = 100) -> str:
        """
        Génère un aperçu du contenu de la note.
        """
        if self.est_chiffree:
            return "🔒 Note chiffrée"
        
        if not self.contenu:
            return ""

        if len(self.contenu) <= longueur_max:
            return self.contenu
            
        return self.contenu[:longueur_max].rsplit(' ', 1)[0] + "..."

    @staticmethod
    def rechercher(session: Session, requete: str):
        """
        Recherche des notes par titre ou contenu.
        """
        return session.query(Note).filter(
            or_(
                Note.titre.ilike(f"%{requete}%"),
                Note.contenu.ilike(f"%{requete}%")
            )
        )

    @staticmethod
    def obtenir_favoris(session: Session):
        """
        Retourne toutes les notes marquées comme favorites.
        """
        return session.query(Note).filter(Note.est_favoriss == True).all()

    @staticmethod
    def obtenir_par_categorie(session: Session, categorie_instance):
        """
        Retourne toutes les notes d'une catégorie spécifique.
        """
        return session.query(Note).filter(Note.id_categorie == categorie_instance.identifiant).all()
