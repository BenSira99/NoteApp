"""
Modèle PieceJointe pour stocker les fichiers attachés aux notes.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from .base_de_donnees import Base

class PieceJointe(Base):
    """
    Modèle représentant un fichier attaché à une note.
    """
    __tablename__ = "pieces_jointes"

    identifiant = Column(Integer, primary_key=True)
    id_note = Column(Integer, ForeignKey("notes.identifiant", ondelete="CASCADE"), nullable=False)
    chemin_acces = Column(String(500), nullable=False)
    type_fichier = Column(String(100), default="application/octet-stream")
    nom_fichier = Column(String(255), nullable=False)
    date_creation = Column(DateTime, default=datetime.now)

    # Relations
    note = relationship("Note", back_populates="pieces_jointes")

    def __str__(self) -> str:
        return f"{self.nom_fichier} ({self.type_fichier})"

    def est_une_image(self) -> bool:
        """
        Vérifie si la pièce jointe est une image.
        """
        return self.type_fichier.startswith("image/")

    @staticmethod
    def obtenir_par_note(session: Session, note_instance):
        """
        Récupère toutes les pièces jointes d'une note.
        """
        return session.query(PieceJointe).filter(PieceJointe.id_note == note_instance.identifiant).all()
