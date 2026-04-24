"""
Configuration de la base de données NoteApp via SQLAlchemy.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from src.utils.constantes import CHEMIN_BASE_DONNEES
from src.utils.journaliseur import journal

# Classe de base pour tous les modèles
Base = declarative_base()

# Variables globales pour le moteur et la fabrique de sessions
moteur = None
SessionLocale = None

def initialiser_base_de_donnees() -> Session:
    """
    Initialise la base de données SQLite et crée les tables.
    
    Returns:
        Session: Une nouvelle session de base de données.
    """
    global moteur, SessionLocale
    
    journal.info(f"Initialisation de la base de données à : {CHEMIN_BASE_DONNEES}")
    
    # Création du moteur SQLAlchemy
    url_base = f"sqlite:///{CHEMIN_BASE_DONNEES}"
    moteur = create_engine(
        url_base,
        connect_args={"check_same_thread": False},
        echo=False
    )
    
    # Création de la fabrique de sessions
    SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=moteur)
    
    # Import des modèles ici pour éviter les imports circulaires
    from .categorie import Categorie
    from .note import Note
    from .piece_jointe import PieceJointe
    from .modele_parametres import ParametreApplication
    
    # Création effective des tables
    Base.metadata.create_all(bind=moteur)
    journal.info("Base de données initialisée avec succès.")
    
    return SessionLocale()

def obtenir_session() -> Session:
    """
    Retourne une nouvelle session de base de données.
    """
    if SessionLocale is None:
        return initialiser_base_de_donnees()
    return SessionLocale()

def fermer_base_de_donnees() -> None:
    """
    Ferme les connexions au moteur de base de données.
    """
    global moteur
    if moteur:
        moteur.dispose()
        journal.info("Connexion à la base de données fermée.")
