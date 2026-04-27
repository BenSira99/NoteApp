"""
VueEditeur - Écran de création et d'édition de notes.
"""

import flet as ft
from src.models.note import Note
from src.models.categorie import Categorie
from src.models.base_de_donnees import obtenir_session
from src.utils.journaliseur import journal
from src.utils.assistants_ui import afficher_barre_notification

class VueEditeur(ft.Container):
    """
    Écran permettant de rédiger une note, de la catégoriser et de la sécuriser.
    """
    def __init__(self, page: ft.Page, id_note: int = None, au_sauvegarder=None) -> None:
        super().__init__()
        self.page_principale = page
        self.id_note = id_note
        self.au_sauvegarder = au_sauvegarder
        self.session_db = obtenir_session()
        self._note = None
        self._est_favori = False
        self._est_chiffre = False
        
        # Initialisation des composants UI
        self.champ_titre = ft.TextField(
            hint_text="Titre de la note",
            border=ft.InputBorder.NONE,
            text_size=24,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            content_padding=ft.padding.symmetric(horizontal=16, vertical=10),
        )

        self.champ_contenu = ft.TextField(
            hint_text="Commencez à écrire...",
            border=ft.InputBorder.NONE,
            multiline=True,
            min_lines=20,
            max_lines=None,
            expand=True,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=10),
        )

        self.menu_categorie = ft.Dropdown(
            hint_text="Catégorie",
            width=200,
            border_radius=10,
        )
        self._charger_categories()

        self.bouton_favori = ft.IconButton(
            icon=ft.Icons.FAVORITE_BORDER,
            tooltip="Ajouter aux favoris",
            on_click=self._basculer_favori
        )

        self.bouton_chiffrer = ft.IconButton(
            icon=ft.Icons.LOCK_OPEN,
            tooltip="Chiffrer la note",
            on_click=self._basculer_chiffrement
        )

        # Barre d'outils
        barre_outils = ft.Container(
            content=ft.Row([
                self.menu_categorie,
                ft.VerticalDivider(width=1),
                self.bouton_favori,
                self.bouton_chiffrer,
                ft.IconButton(
                    icon=ft.Icons.PICTURE_AS_PDF, 
                    tooltip="Exporter en PDF", 
                    on_click=self._exporter_pdf
                ),
            ], spacing=5),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        )

        # Assemblage
        self.content = ft.Column([
            barre_outils,
            self.champ_titre,
            ft.Divider(height=1),
            self.champ_contenu,
        ], expand=True, spacing=0)
        
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE

        if id_note:
            self._charger_note_existante(id_note)

    def _charger_categories(self) -> None:
        self.menu_categorie.options = [ft.dropdown.Option(key="none", text="Sans catégorie")]
        try:
            categories = self.session_db.query(Categorie).all()
            for cat in categories:
                self.menu_categorie.options.append(ft.dropdown.Option(key=str(cat.identifiant), text=cat.nom))
        except Exception as e:
            journal.error(f"Erreur chargement catégories : {e}")

    def _charger_note_existante(self, id_note: int) -> None:
        try:
            self._note = self.session_db.query(Note).filter(Note.identifiant == id_note).first()
            if self._note:
                self.champ_titre.value = self._note.titre
                self.champ_contenu.value = self._note.contenu
                if self._note.id_categorie:
                    self.menu_categorie.value = str(self._note.id_categorie)
                self._est_favori = self._note.est_favoris
                self._mettre_a_jour_bouton_favori()
                self._est_chiffre = self._note.est_chiffree
                self._mettre_a_jour_bouton_chiffrement()
        except Exception as e:
            journal.error(f"Erreur chargement note : {e}")

    def _basculer_favori(self, e) -> None:
        self._est_favori = not self._est_favori
        self._mettre_a_jour_bouton_favori()
        self.update()

    def _mettre_a_jour_bouton_favori(self) -> None:
        self.bouton_favori.icon = ft.Icons.FAVORITE if self._est_favori else ft.Icons.FAVORITE_BORDER
        self.bouton_favori.icon_color = ft.Colors.RED if self._est_favori else None

    def _basculer_chiffrement(self, e) -> None:
        self._est_chiffre = not self._est_chiffre
        self._mettre_a_jour_bouton_chiffrement()
        self.update()

    def _mettre_a_jour_bouton_chiffrement(self) -> None:
        self.bouton_chiffrer.icon = ft.Icons.LOCK if self._est_chiffre else ft.Icons.LOCK_OPEN
        self.bouton_chiffrer.icon_color = ft.Colors.AMBER if self._est_chiffre else None

    def sauvegarder(self) -> bool:
        """Méthode appelée par l'application pour enregistrer la note."""
        titre = self.champ_titre.value.strip() if self.champ_titre.value else ""
        contenu = self.champ_contenu.value.strip() if self.champ_contenu.value else ""

        if not titre:
            afficher_barre_notification(self.page_principale, "Le titre est obligatoire !", est_erreur=True)
            return False

        id_cat = None if not self.menu_categorie.value or self.menu_categorie.value == "none" else int(self.menu_categorie.value)

        try:
            if self._note:
                self._note.titre = titre
                self._note.contenu = contenu
                self._note.id_categorie = id_cat
                self._note.est_favoris = self._est_favori
                self._note.est_chiffree = self._est_chiffre
            else:
                nueva_note = Note(
                    titre=titre,
                    contenu=contenu,
                    id_categorie=id_cat,
                    est_favoris=self._est_favori,
                    est_chiffree=self._est_chiffre
                )
                self.session_db.add(nueva_note)
            
            self.session_db.commit()
            journal.success(f"Note '{titre}' sauvegardée.")
            return True
        except Exception as e:
            journal.error(f"Erreur sauvegarde base de données : {e}")
            self.session_db.rollback()
            return False

    def _exporter_pdf(self, e) -> None:
        """Export PDF natif via Tkinter."""
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        titre = self.champ_titre.value or "Sans_titre"
        nom_defaut = f"{titre.replace(' ', '_')}.pdf"
        
        chemin = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Fichiers PDF", "*.pdf")],
            initialfile=nom_defaut,
            title="Exporter en PDF"
        )
        root.destroy()
        
        if not chemin:
            return

        nom_cat = None
        if self.menu_categorie.value and self.menu_categorie.value != "none":
            cat = self.session_db.query(Categorie).get(int(self.menu_categorie.value))
            nom_cat = cat.nom if cat else None

        from src.services.export_pdf import obtenir_service_pdf
        try:
            pdf_service = obtenir_service_pdf()
            pdf_service.exporter_note(
                titre=titre,
                contenu=self.champ_contenu.value or "",
                chemin_complet=chemin,
                categorie=nom_cat,
                date_creation=self._note.date_creation if self._note else None
            )
            afficher_barre_notification(self.page_principale, f"PDF créé : {chemin}")
        except Exception as ex:
            journal.error(f"Erreur export PDF : {ex}")
            afficher_barre_notification(self.page_principale, "Erreur export PDF", est_erreur=True)
