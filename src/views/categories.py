"""
VueCategories - Gestion des catégories de notes.
"""

import flet as ft
from src.models.categorie import Categorie
from src.models.base_de_donnees import obtenir_session
from src.utils.constantes import Couleurs, Icones
from src.utils.journaliseur import journal
from src.utils.assistants_ui import afficher_dialogue, fermer_dialogue, afficher_barre_notification

class VueCategories(ft.Container):
    """
    Vue permettant de gérer (ajouter, modifier, supprimer) les catégories.
    """
    def __init__(self, page: ft.Page, au_retour=None) -> None:
        super().__init__()
        self.page_principale = page
        self.au_retour = au_retour
        self.session_db = obtenir_session()
        
        # Liste des catégories
        self.liste_categories = ft.ListView(
            expand=True,
            spacing=8,
            padding=16,
        )
        
        self.content = self.liste_categories
        self.expand = True
        
        self._charger_categories()

    def _charger_categories(self) -> None:
        """Charge et affiche les catégories depuis la base de données."""
        self.liste_categories.controls.clear()
        categories = self.session_db.query(Categorie).all()
        
        for cat in categories:
            element = self._creer_element_categorie(cat)
            self.liste_categories.controls.append(element)
            
        try:
            self.liste_categories.update()
        except Exception:
            pass

    def _creer_element_categorie(self, categorie: Categorie) -> ft.Container:
        """Crée un élément de liste pour une catégorie."""
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Container(
                    content=ft.Icon(
                        getattr(ft.Icons, categorie.icone.upper(), ft.Icons.FOLDER),
                        color=ft.Colors.WHITE,
                        size=20,
                    ),
                    bgcolor=categorie.couleur,
                    border_radius=8,
                    width=36,
                    height=36,
                    alignment=ft.Alignment(0, 0),
                    on_click=lambda _, c=categorie: self.afficher_dialogue_edition(c),
                ),
                title=ft.Text(categorie.nom, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(
                    f"{len(categorie.notes)} notes",
                    size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                trailing=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.Icons.EDIT, size=18),
                                ft.Text("Modifier"),
                            ], spacing=10),
                            on_click=lambda _: self.afficher_dialogue_edition(categorie),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(ft.Icons.DELETE, size=18),
                                ft.Text("Supprimer"),
                            ], spacing=10),
                            on_click=lambda _: self._supprimer_categorie(categorie),
                        ),
                    ],
                ),
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=12,
        )

    def afficher_dialogue_ajout(self) -> None:
        """Affiche le dialogue pour ajouter une nouvelle catégorie."""
        champ_nom = ft.TextField(label="Nom de la catégorie", autofocus=True)
        selecteur_couleur = ft.Dropdown(
            label="Couleur",
            value=Couleurs.COULEURS_CATEGORIES[0],
            options=[
                ft.dropdown.Option(
                    key=c,
                    content=ft.Row([
                        ft.Icon(ft.Icons.CIRCLE, color=c, size=16),
                        ft.Text("Couleur " + str(i+1))
                    ], spacing=10)
                ) for i, c in enumerate(Couleurs.COULEURS_CATEGORIES)
            ],
        )

        def sauvegarder_nouvelle(e):
            nom = champ_nom.value.strip()
            if not nom: return
            try:
                nouvelle_cat = Categorie(
                    nom=nom,
                    couleur=selecteur_couleur.value,
                    icone="folder"
                )
                self.session_db.add(nouvelle_cat)
                self.session_db.commit()
                fermer_dialogue(self.page_principale)
                self._charger_categories()
                journal.success(f"Catégorie créée : {nom}")
            except Exception as ex:
                journal.error(f"Erreur création catégorie : {ex}")

        dialogue = ft.AlertDialog(
            title=ft.Text("Nouvelle catégorie"),
            content=ft.Column([champ_nom, selecteur_couleur], tight=True),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: fermer_dialogue(self.page_principale)),
                ft.TextButton("Créer", on_click=sauvegarder_nouvelle),
            ],
        )
        afficher_dialogue(self.page_principale, dialogue)

    def afficher_dialogue_edition(self, categorie: Categorie) -> None:
        """Affiche le dialogue pour modifier une catégorie existante."""
        champ_nom = ft.TextField(label="Nom de la catégorie", value=categorie.nom, autofocus=True)
        selecteur_couleur = ft.Dropdown(
            label="Couleur",
            value=categorie.couleur,
            options=[
                ft.dropdown.Option(key=c) for c in Couleurs.COULEURS_CATEGORIES
            ],
        )

        def enregistrer_modifs(e):
            nom = champ_nom.value.strip()
            if not nom: return
            try:
                categorie.nom = nom
                categorie.couleur = selecteur_couleur.value
                self.session_db.commit()
                fermer_dialogue(self.page_principale)
                self._charger_categories()
            except Exception as ex:
                journal.error(f"Erreur modification catégorie : {ex}")

        dialogue = ft.AlertDialog(
            title=ft.Text("Modifier la catégorie"),
            content=ft.Column([champ_nom, selecteur_couleur], tight=True),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: fermer_dialogue(self.page_principale)),
                ft.TextButton("Enregistrer", on_click=enregistrer_modifs),
            ],
        )
        afficher_dialogue(self.page_principale, dialogue)

    def _supprimer_categorie(self, categorie: Categorie) -> None:
        """Demande confirmation et supprime la catégorie."""
        def confirmer(e):
            try:
                self.session_db.delete(categorie)
                self.session_db.commit()
                fermer_dialogue(self.page_principale)
                self._charger_categories()
                afficher_barre_notification(self.page_principale, f"Catégorie '{categorie.nom}' supprimée")
            except Exception as ex:
                journal.error(f"Erreur suppression catégorie : {ex}")

        dialogue = ft.AlertDialog(
            title=ft.Text("Supprimer la catégorie ?"),
            content=ft.Text(f"Voulez-vous vraiment supprimer '{categorie.nom}' ?"),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: fermer_dialogue(self.page_principale)),
                ft.TextButton("Supprimer", on_click=confirmer, color=ft.Colors.ERROR),
            ],
        )
        afficher_dialogue(self.page_principale, dialogue)

