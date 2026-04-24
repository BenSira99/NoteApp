"""
Composant BarreRecherche - Entrée de recherche réutilisable avec filtrage.
"""

import flet as ft
from src.utils.constantes import COULEUR_ACCENT

class BarreRecherche(ft.Container):
    """
    Un composant de barre de recherche avec icône et bouton de nettoyage.
    """
    def __init__(
        self,
        texte_indicatif: str = "Rechercher...",
        sur_changement=None,
        sur_soumission=None,
    ) -> None:
        self._sur_changement = sur_changement
        self._sur_soumission = sur_soumission
        
        self.champ_recherche = ft.TextField(
            hint_text=texte_indicatif,
            prefix_icon=ft.Icons.SEARCH,
            border_radius=25,
            filled=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_color=ft.Colors.TRANSPARENT,
            focused_border_color=COULEUR_ACCENT,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
            text_size=14,
            on_change=self._gerer_changement,
            on_submit=self._gerer_soumission,
            expand=True,
        )
        
        self.bouton_nettoyer = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.ON_SURFACE_VARIANT,
            icon_size=18,
            visible=False,
            on_click=self._nettoyer_recherche,
            tooltip="Effacer",
        )
        
        super().__init__(
            content=ft.Row(
                [
                    self.champ_recherche,
                    self.bouton_nettoyer,
                ],
                spacing=0,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
        )

    def _gerer_changement(self, e: ft.ControlEvent) -> None:
        """
        Gère l'événement de changement de texte.
        """
        self.bouton_nettoyer.visible = bool(e.control.value)
        self.bouton_nettoyer.update()
        if self._sur_changement:
            self._sur_changement(e.control.value)

    def _gerer_soumission(self, e: ft.ControlEvent) -> None:
        """
        Gère l'événement de soumission du formulaire.
        """
        if self._sur_soumission:
            self._sur_soumission(e.control.value)

    def _nettoyer_recherche(self, e: ft.ControlEvent) -> None:
        """
        Efface le contenu du champ de recherche.
        """
        self.champ_recherche.value = ""
        self.champ_recherche.update()
        self.bouton_nettoyer.visible = False
        self.bouton_nettoyer.update()
        if self._sur_changement:
            self._sur_changement("")

    @property
    def valeur(self) -> str:
        """
        Retourne la valeur actuelle de la recherche.
        """
        return self.champ_recherche.value or ""

