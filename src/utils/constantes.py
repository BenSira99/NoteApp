"""
Constantes et configuration de l'application NoteApp.
Lieu central pour les couleurs, les dimensions et les réglages.
"""

import os

class Couleurs:
    """Palette de couleurs de l'application (Style Cyber-Dark)."""
    # Couleurs primaires
    PRIMAIRE = "#6200EE"
    PRIMAIRE_VARIANTE = "#3700B3"
    SECONDAIRE = "#03DAC6"
    SECONDAIRE_VARIANTE = "#018786"
    
    # Couleurs de fond
    FOND_CLAIR = "#FFFFFF"
    FOND_SOMBRE = "#121212"
    SURFACE_CLAIRE = "#F5F5F5"
    SURFACE_SOMBRE = "#1E1E1E"
    
    # Couleurs d'état
    ERREUR = "#B00020"
    SUCCES = "#4CAF50"
    AVERTISSEMENT = "#FFC107"
    INFO = "#2196F3"
    
    # Couleurs de texte
    TEXTE_PRIMAIRE_CLAIR = "#212121"
    TEXTE_SECONDAIRE_CLAIR = "#757575"
    TEXTE_PRIMAIRE_SOMBRE = "#FFFFFF"
    TEXTE_SECONDAIRE_SOMBRE = "#B0B0B0"
    
    # Couleurs par défaut des catégories
    COULEURS_CATEGORIES = [
        "#6200EE", # Violet
        "#03DAC6", # Turquoise
        "#FFC107", # Ambre
        "#4CAF50", # Vert
        "#F44336", # Rouge
        "#2196F3", # Bleu
        "#FF9800", # Orange
        "#9C27B0", # Pourpre
    ]

# Raccourcis pour l'accessibilité Ben Sira (Cyber-Dark Luxury)
COULEUR_ACCENT = Couleurs.PRIMAIRE
COULEUR_DANGER = Couleurs.ERREUR
COULEUR_SECONDAIRE = Couleurs.SECONDAIRE
COULEUR_TEXTE_PRINCIPAL = Couleurs.TEXTE_PRIMAIRE_SOMBRE
COULEUR_TEXTE_SECONDAIRE = Couleurs.TEXTE_SECONDAIRE_SOMBRE

class ConfigurationApp:
    """Réglages de configuration de l'application."""
    # Infos App
    NOM_APPLICATION = "Note App"
    VERSION_APPLICATION = "1.0.0"
    
    # Base de données
    NOM_BASE_DONNEES = "notes.db"
    
    # Réglages UI
    THEME_PAR_DEFAUT = "dark" # On privilégie le mode sombre
    
    # Réglages Notes
    LONGUEUR_MAX_TITRE = 200
    LONGUEUR_APERÇU = 100
    
    # Sécurité
    LONGUEUR_PIN_MIN = 4
    LONGUEUR_PIN_MAX = 6
    TENTATIVES_MAX_CONNEXION = 5
    DUREE_VERROUILLAGE_SECONDES = 300 # 5 minutes
    
    # Chiffrement
    ALGORITHME_CHIFFREMENT = "AES-256-GCM"
    
    # Limites fichiers
    TAILLE_MAX_IMAGE_MO = 10
    TAILLE_MAX_PIECE_JOINTE_MO = 25
    
    # Réglages Rappels
    HEURE_RAPPEL_DEFAUT = 9 # 9h00
    MINUTE_RAPPEL_DEFAUT = 0

class Icones:
    """Noms des icônes Material Design utilisées."""
    # Navigation
    ACCUEIL = "home"
    PARAMETRES = "settings"
    RETOUR = "arrow_back"
    
    # Notes
    NOTE = "note"
    AJOUT_NOTE = "note_add"
    MODIFIER = "edit"
    SUPPRIMER = "delete"
    
    # Catégories
    DOSSIER = "folder"
    CATEGORIE = "category"
    
    # Actions
    RECHERCHE = "search"
    FAVORIS = "favorite"
    FAVORIS_BORDURE = "favorite_border"
    VERROU = "lock"
    VERROU_OUVERT = "lock_open"
    PARTAGE = "share"
    PDF = "picture_as_pdf"
    
    # Statuts
    VALIDER = "check"
    FERMER = "close"
    AVERTISSEMENT = "warning"
    INFO = "info"

# Chemins système
CHEMIN_SRC = os.path.dirname(os.path.dirname(__file__))
CHEMIN_DATA = os.path.join(CHEMIN_SRC, "data")
CHEMIN_BASE_DONNEES = os.path.join(CHEMIN_DATA, ConfigurationApp.NOM_BASE_DONNEES)

# Assurer l'existence du dossier data
os.makedirs(CHEMIN_DATA, exist_ok=True)

# Alias pour export
TITRE_APPLICATION = ConfigurationApp.NOM_APPLICATION
