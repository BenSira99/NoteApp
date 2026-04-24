"""
Composant CarteNote - Affiche un aperçu d'une note dans la liste.
"""

import flet as ft
from datetime import datetime
from src.utils.constantes import COULEUR_ACCENT, COULEUR_DANGER, COULEUR_TEXTE_PRINCIPAL, COULEUR_TEXTE_SECONDAIRE

class CarteNote(ft.Container):
    """
    Un composant de carte affichant un aperçu de note.
    Affiche le titre, l'aperçu du contenu, la catégorie et le statut de favoris.
    """
    def __init__(
        self,
        id_note: int,
        titre: str,
        aperçu: str,
        nom_categorie: str = None,
        couleur_categorie: str = None,
        est_favoris: bool = False,
        est_chiffree: bool = False,
        date_mise_a_jour: datetime = None,
        sur_clic=None,
        sur_clic_favori=None,
        sur_clic_supprimer=None,
    ) -> None:
        self.id_note = id_note
        self._sur_clic_carte = sur_clic
        self._sur_clic_favori = sur_clic_favori
        self._sur_clic_supprimer = sur_clic_supprimer

        # Formatage de la date
        texte_date = ""
        if date_mise_a_jour:
            maintenant = datetime.now()
            if date_mise_a_jour.date() == maintenant.date():
                texte_date = date_mise_a_jour.strftime("%H:%M")
            else:
                texte_date = date_mise_a_jour.strftime("%d/%m/%Y")

        # Puce de catégorie
        puce_categorie = None
        if nom_categorie:
            puce_categorie = ft.Container(
                content=ft.Text(
                    nom_categorie,
                    size=10,
                    color=ft.Colors.WHITE,
                ),
                bgcolor=couleur_categorie or COULEUR_ACCENT,
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=8, vertical=2),
            )

        # Icône de favoris
        icone_favoris = ft.IconButton(
            icon=ft.Icons.FAVORITE if est_favoris else ft.Icons.FAVORITE_BORDER,
            icon_color=COULEUR_DANGER if est_favoris else ft.Colors.ON_SURFACE_VARIANT,
            icon_size=20,
            on_click=self._gerer_clic_favoris,
            tooltip="Favoris",
        )

        # Icône de verrou pour les notes chiffrées
        icone_verrou = None
        if est_chiffree:
            icone_verrou = ft.Icon(
                ft.Icons.LOCK,
                size=16,
                color=ft.Colors.AMBER,
            )

        # Construction du contenu de la carte
        contenu_carte = ft.Column(
            [
                # Ligne d'en-tête (titre + icônes)
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    titre,
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.ON_SURFACE,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True,
                                ),
                                icone_verrou if icone_verrou else ft.Container(),
                            ],
                            expand=True,
                            spacing=5,
                        ),
                        icone_favoris,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                # Texte d'aperçu
                ft.Text(
                    aperçu,
                    size=13,
                    color=COULEUR_TEXTE_SECONDAIRE,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                # Ligne de pied de page (catégorie + date)
                ft.Row(
                    [
                        puce_categorie if puce_categorie else ft.Container(),
                        ft.Text(
                            texte_date,
                            size=11,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=8,
        )

        super().__init__(
            content=contenu_carte,
            padding=15,
            border_radius=12,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            on_click=self._gerer_clic_carte,
            ink=True,
        )

    def _gerer_clic_carte(self, e: ft.ControlEvent) -> None:
        """
        Gère l'événement de clic sur la carte.
        """
        if self._sur_clic_carte:
            self._sur_clic_carte(self.id_note)

    def _gerer_clic_favoris(self, e: ft.ControlEvent) -> None:
        """
        Gère l'événement de clic sur le bouton favoris.
        """
        if self._sur_clic_favori:
            self._sur_clic_favori(self.id_note)

