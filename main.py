"""
NoteApp - Point d'entrée principal (Racine).
Ce fichier sert de pivot pour éviter les problèmes de PYTHONPATH.
"""

import flet as ft
from src.app import principal

if __name__ == "__main__":
    # Point d'entrée de l'application
    # assets_dir pointe vers le dossier contenant les images/logos
    ft.run(principal, assets_dir="src/assets")
