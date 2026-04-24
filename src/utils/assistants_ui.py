"""
Assistants UI - Fonctions d'aide pour l'interface utilisateur Flet (Compatibilité 0.80.0+).
"""

import flet as ft
from src.utils.constantes import COULEUR_ACCENT

def afficher_dialogue(page: ft.Page, dialogue: ft.AlertDialog) -> None:
    """Affiche une boîte de dialogue en utilisant l'API Flet moderne."""
    page.show_dialog(dialogue)

def fermer_dialogue(page: ft.Page, dialogue: ft.AlertDialog = None) -> None:
    """Ferme la boîte de dialogue actuelle."""
    page.pop_dialog()

def afficher_barre_notification(page: ft.Page, message: str, est_erreur: bool = False, duree: int = 3000) -> None:
    """
    Affiche une barre de notification (SnackBar).
    
    Args:
        page (ft.Page): La page Flet.
        message (str): Le texte à afficher.
        est_erreur (bool): Si True, affiche en rouge.
        duree (int): Durée d'affichage en ms.
    """
    couleur_fond = ft.Colors.ERROR if est_erreur else COULEUR_ACCENT
    
    snackbar = ft.SnackBar(
        content=ft.Text(message, color=ft.Colors.WHITE),
        bgcolor=couleur_fond,
        duration=duree,
        action="OK"
    )
    
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()

def basculer_theme(page: ft.Page) -> None:
    """Bascule entre le mode clair et le mode sombre."""
    page.theme_mode = (
        ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    )
    page.update()
