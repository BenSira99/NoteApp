"""
Composant PuceCategorie - Petite puce colorée pour l'affichage des catégories.
"""

import flet as ft
from src.utils.constantes import COULEUR_ACCENT

class PuceCategorie(ft.Container):
    """
    Un petit composant de type puce pour afficher une catégorie.
    """
    def __init__(
        self,
        nom: str,
        couleur: str = None,
        selectionnee: bool = False,
        sur_clic=None,
    ) -> None:
        self.nom = nom
        self._selectionnee = selectionnee
        self._sur_clic = sur_clic
        
        couleur_puce = couleur or COULEUR_ACCENT
        
        éléments_contenu = [
            ft.Text(
                nom,
                size=12,
                color=ft.Colors.WHITE if selectionnee else couleur_puce,
                weight=ft.FontWeight.W_500,
            )
        ]
        
        super().__init__(
            content=ft.Row(
                éléments_contenu,
                spacing=4,
            ),
            bgcolor=couleur_puce if selectionnee else ft.Colors.with_opacity(0.1, couleur_puce),
            border=ft.border.all(1, couleur_puce),
            border_radius=15,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            on_click=self._gerer_clic,
            ink=True,
        )

    def _gerer_clic(self, e: ft.ControlEvent) -> None:
        """
        Gère l'événement de clic sur la puce.
        """
        if self._sur_clic:
            self._sur_clic(self.nom)

    @property
    def selectionnee(self) -> bool:
        """
        Retourne l'état de sélection de la puce.
        """
        return self._selectionnee

    @selectionnee.setter
    def selectionnee(self, valeur: bool) -> None:
        """
        Définit l'état de sélection et met à jour l'apparence.
        """
        self._selectionnee = valeur
        self.update()
