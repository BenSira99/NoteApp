"""
Configuration du journaliseur utilisant Loguru.
Fournit une journalisation structurée, colorée et persistante.
"""

import sys
import os
from loguru import logger

# Suppression du gestionnaire par défaut
logger.remove()

# Ajout du gestionnaire console avec un format personnalisé
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)

def configurer_journalisation_fichier(dossier_logs: str = None) -> None:
    """
    Configure la journalisation dans des fichiers.
    
    Args:
        dossier_logs: Dossier où stocker les logs. Par défaut 'logs' à la racine.
    """
    if dossier_logs is None:
        chemin_parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        dossier_logs = os.path.join(chemin_parent, "logs")
        
    os.makedirs(dossier_logs, exist_ok=True)
    
    logger.add(
        os.path.join(dossier_logs, "application_{time:YYYY-MM-DD}.log"),
        rotation="1 day",      # Nouveau fichier chaque jour
        retention="7 jours",   # Garde les logs pendant 7 jours
        compression="zip",     # Compresse les anciens logs
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    logger.info("Journalisation fichier initialisée.")

# Alias francophone pour export
journal = logger

def journaliser_erreur(message: str) -> None:
    """Helper simple pour journaliser une erreur."""
    journal.error(message)

def journaliser_succes(message: str) -> None:
    """Helper simple pour journaliser un succès."""
    journal.success(message)

# Exportation du logger configuré
__all__ = ["journal", "configurer_journalisation_fichier"]
