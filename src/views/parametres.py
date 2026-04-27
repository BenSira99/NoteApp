"""
Vue des paramètres - NoteApp.
Permet de configurer l'application, le thème et la sécurité.
"""

import flet as ft
from src.models.base_de_donnees import obtenir_session
from src.services.service_authentification import obtenir_service_authentification
from src.utils.journaliseur import journal
from src.utils.assistants_ui import afficher_barre_notification, afficher_dialogue
from src.models.note import Note
from src.models.categorie import Categorie
import json
from datetime import datetime

class VueParametres(ft.Column):
    """
    Composant gérant les réglages de l'application.
    """
    def __init__(self, page_principale: ft.Page, au_retour=None) -> None:
        super().__init__()
        self.page_principale = page_principale
        self.au_retour = au_retour
        self.session_db = obtenir_session()
        self.authentification = obtenir_service_authentification()
        
        # Sélections et interrupteurs
        self.interrupteur_theme = ft.Switch(
            label="Thème sombre",
            value=self.page_principale.theme_mode == ft.ThemeMode.DARK,
            on_change=self._sur_changement_theme,
        )

        # Construction des sections
        section_apparence = self._creer_section(
            "Apparence",
            [self.interrupteur_theme]
        )

        section_securite = self._creer_section(
            "Sécurité",
            [
                self._creer_item_reglage(
                    ft.Icons.LOCK,
                    "Configurer le PIN",
                    "Protéger l'accès à vos notes",
                    on_click=self._configurer_pin
                )
            ]
        )

        section_donnees = self._creer_section(
            "Données",
            [
                self._creer_item_reglage(
                    ft.Icons.FILE_DOWNLOAD,
                    "Exporter (JSON)",
                    "Sauvegarder toutes vos notes",
                    on_click=self._exporter_json
                ),
                self._creer_item_reglage(
                    ft.Icons.FILE_UPLOAD,
                    "Importer (JSON)",
                    "Restaurer vos notes depuis un fichier",
                    on_click=self._importer_json
                ),
                self._creer_item_reglage(
                    ft.Icons.DELETE_FOREVER,
                    "Effacer tout",
                    "Supprimer toutes les notes et catégories",
                    couleur=ft.Colors.ERROR,
                    on_click=self._confirmer_suppression_totale
                )
            ]
        )

        # Assemblage final
        self.controls = [
            ft.Text("Paramètres", size=32, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            section_apparence,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            section_securite,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            section_donnees,
        ]
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True

    def _creer_section(self, titre: str, items: list) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Text(titre, size=18, weight=ft.FontWeight.W_600, color=ft.Colors.ACCENT),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(items, spacing=5),
                        padding=10
                    )
                )
            ]),
            margin=ft.margin.only(bottom=20)
        )

    def _creer_item_reglage(self, icone, titre, description, on_click=None, couleur=None) -> ft.ListTile:
        return ft.ListTile(
            leading=ft.Icon(icone, color=couleur if couleur else ft.Colors.PRIMARY),
            title=ft.Text(titre, weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(description, size=12),
            on_click=on_click
        )

    def _sur_changement_theme(self, e) -> None:
        self.page_principale.theme_mode = (
            ft.ThemeMode.DARK if self.interrupteur_theme.value else ft.ThemeMode.LIGHT
        )
        self.page_principale.update()
        journal.info(f"Thème changé en {'sombre' if self.interrupteur_theme.value else 'clair'}")

    def _configurer_pin(self, e) -> None:
        # Implémentation simplifiée pour l'instant
        afficher_barre_notification(self.page_principale, "Fonctionnalité PIN bientôt disponible")

    def _exporter_json(self, e) -> None:
        """Déclenche l'exportation des données via un sélecteur natif Tkinter."""
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        nom_defaut = f"sauvegarde_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        chemin = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json")],
            initialfile=nom_defaut,
            title="Exporter les notes"
        )
        root.destroy()
        
        if not chemin:
            return

        try:
            notes = self.session_db.query(Note).all()
            data = [
                {
                    "titre": n.titre,
                    "contenu": n.contenu,
                    "categorie": n.categorie.nom if n.categorie else None,
                    "est_favoris": n.est_favoris,
                    "est_chiffree": n.est_chiffree,
                    "date_creation": n.date_creation.isoformat() if n.date_creation else None
                } 
                for n in notes
            ]
            
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            afficher_barre_notification(self.page_principale, "Exportation réussie !")
            journal.success(f"Données exportées dans {chemin}")
        except Exception as ex:
            journal.error(f"Échec export JSON : {ex}")
            afficher_barre_notification(self.page_principale, "Erreur lors de l'exportation", est_erreur=True)

    def _importer_json(self, e) -> None:
        """Déclenche l'importation des données via un sélecteur natif Tkinter."""
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        chemin = filedialog.askopenfilename(
            filetypes=[("Fichiers JSON", "*.json")],
            title="Importer des notes"
        )
        root.destroy()
        
        if not chemin:
            return

        try:
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for item in data:
                id_cat = None
                if item.get("categorie"):
                    cat = self.session_db.query(Categorie).filter(Categorie.nom == item["categorie"]).first()
                    if not cat:
                        cat = Categorie(nom=item["categorie"])
                        self.session_db.add(cat)
                        self.session_db.flush()
                    id_cat = cat.identifiant
                
                nouvelle_note = Note(
                    titre=item["titre"],
                    contenu=item["contenu"],
                    id_categorie=id_cat,
                    est_favoris=item.get("est_favoris", False),
                    est_chiffree=item.get("est_chiffree", False)
                )
                self.session_db.add(nouvelle_note)
            
            self.session_db.commit()
            afficher_barre_notification(self.page_principale, f"{len(data)} notes importées !")
            if self.au_retour:
                self.au_retour()
        except Exception as ex:
            journal.error(f"Échec import JSON : {ex}")
            afficher_barre_notification(self.page_principale, "Fichier de sauvegarde invalide", est_erreur=True)

    def _confirmer_suppression_totale(self, e) -> None:
        dialogue = ft.AlertDialog(
            title=ft.Text("Supprimer tout ?"),
            content=ft.Text("Cette action est irréversible. Toutes vos notes seront perdues."),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: self.page_principale.close_dialog()),
                ft.TextButton("Tout supprimer", color=ft.Colors.ERROR, on_click=self._supprimer_tout)
            ]
        )
        afficher_dialogue(self.page_principale, dialogue)

    def _supprimer_tout(self, e) -> None:
        try:
            self.session_db.query(Note).delete()
            self.session_db.query(Categorie).delete()
            self.session_db.commit()
            self.page_principale.close_dialog()
            afficher_barre_notification(self.page_principale, "Tout a été effacé.")
            if self.au_retour:
                self.au_retour()
        except Exception as ex:
            journal.error(f"Erreur suppression totale : {ex}")
