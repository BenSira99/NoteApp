"""
VueParametres - Écran de configuration et de maintenance.
Gestion du PIN, des thèmes et de la sauvegarde JSON.
"""

import flet as ft
import json
import os
from datetime import datetime
from src.utils.constantes import Couleurs, ConfigurationApp
from src.utils.journaliseur import journal
from src.utils.assistants_ui import (
    afficher_dialogue, 
    fermer_dialogue, 
    afficher_barre_notification, 
    basculer_theme
)
from src.models.note import Note
from src.models.categorie import Categorie
from src.models.base_de_donnees import obtenir_session
from src.services.service_authentification import obtenir_service_authentification

class VueParametres(ft.Container):
    """
    Écran permettant de configurer l'application et de gérer les données.
    """
    def __init__(self, page: ft.Page, au_retour=None) -> None:
        super().__init__()
        self.page_principale = page
        self.au_retour = au_retour
        self.session_db = obtenir_session()
        self.authentification = obtenir_service_authentification()
        
        # Récupération des références nommées depuis l'application (Stabilité Flet 0.84.0)
        self.selecteur_export = self.page_principale.app_instance.selecteur_export_json
        self.selecteur_import = self.page_principale.app_instance.selecteur_import_json
        
        # Assignation des callbacks
        self.selecteur_export.on_result = self._sur_resultat_export_json
        self.selecteur_import.on_result = self._sur_resultat_import_json

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
                    "Protéger l'accès à l'application",
                    sur_clic=self._configurer_le_pin
                ),
            ]
        )

        section_donnees = self._creer_section(
            "Données & Maintenance",
            [
                self._creer_item_reglage(
                    ft.Icons.BACKUP,
                    "Exporter (JSON)",
                    "Sauvegarder toutes les notes localement",
                    sur_clic=self._exporter_json
                ),
                self._creer_item_reglage(
                    ft.Icons.RESTORE,
                    "Importer (JSON)",
                    "Restaurer des notes depuis une sauvegarde",
                    sur_clic=self._importer_json
                ),
            ]
        )

        self.content = ft.ListView(
            controls=[
                section_apparence,
                section_securite,
                section_donnees,
                ft.Container(
                    content=ft.Text(f"Version {ConfigurationApp.VERSION_APPLICATION}", size=12, color=ft.Colors.GREY_600),
                    alignment=ft.Alignment(0, 0),
                    padding=20
                )
            ],
            spacing=20,
            padding=16,
        )
        self.expand = True

    def _creer_section(self, titre: str, items: list) -> ft.Container:
        """Crée une section stylisée avec titre."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(titre, size=14, weight=ft.FontWeight.BOLD, color=Couleurs.PRIMAIRE),
                    ft.Container(
                        content=ft.Column(items, spacing=0),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        border_radius=12,
                        padding=5,
                    ),
                ],
                spacing=8,
            ),
        )

    def _creer_item_reglage(self, icone: str, titre: str, sous_titre: str, sur_clic=None) -> ft.Container:
        """Crée un élément de réglage cliquable."""
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(icone, color=Couleurs.PRIMAIRE),
                title=ft.Text(titre, size=14),
                subtitle=ft.Text(sous_titre, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                trailing=ft.Icons.CHEVRON_RIGHT,
                on_click=sur_clic,
            ),
            ink=True,
            border_radius=8,
        )

    def _sur_changement_theme(self, e) -> None:
        basculer_theme(self.page_principale)
        journal.info(f"Thème changé : {self.page_principale.theme_mode}")

    def _configurer_le_pin(self, e) -> None:
        """Ouvre le dialogue de configuration du PIN."""
        champ_pin = ft.TextField(label="Nouveau PIN (4-6 chiffres)", password=True, can_reveal_password=True, keyboard_type=ft.KeyboardType.NUMBER, max_length=6)
        champ_confirm = ft.TextField(label="Confirmer le PIN", password=True, can_reveal_password=True, keyboard_type=ft.KeyboardType.NUMBER, max_length=6)
        
        def valider(ev):
            if champ_pin.value == champ_confirm.value and len(champ_pin.value) >= 4:
                self.authentification.definir_pin(champ_pin.value)
                fermer_dialogue(self.page_principale)
                afficher_barre_notification(self.page_principale, "Code PIN configuré !")
            else:
                afficher_barre_notification(self.page_principale, "Les codes ne correspondent pas ou sont trop courts.", est_erreur=True)

        dialogue = ft.AlertDialog(
            title=ft.Text("Sécuriser l'application"),
            content=ft.Column([champ_pin, champ_confirm], tight=True),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: fermer_dialogue(self.page_principale)),
                ft.TextButton("Enregistrer", on_click=valider),
            ],
        )
        afficher_dialogue(self.page_principale, dialogue)

    def _exporter_json(self, e) -> None:
        """Déclenche l'exportation des données en JSON."""
        nom_defaut = f"sauvegarde_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.selecteur_export.save_file(
            file_name=nom_defaut,
            allowed_extensions=["json"]
        )

    def _importer_json(self, e) -> None:
        """Déclenche l'importation des données depuis un JSON."""
        self.selecteur_import.pick_files(
            allowed_extensions=["json"]
        )

    def _sur_resultat_export_json(self, e: ft.FilePickerResultEvent) -> None:
        """Finalise l'exportation JSON une fois le chemin choisi."""
        if not e.path:
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
            
            with open(e.path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            afficher_barre_notification(self.page_principale, "Exportation réussie !")
            journal.success(f"Données exportées dans {e.path}")
        except Exception as ex:
            journal.error(f"Échec export JSON : {ex}")
            afficher_barre_notification(self.page_principale, "Erreur lors de l'exportation", est_erreur=True)

    def _sur_resultat_import_json(self, e: ft.FilePickerResultEvent) -> None:
        """Traite le fichier JSON sélectionné pour l'importation."""
        if not e.files:
            return
        
        chemin_fichier = e.files[0].path
        try:
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                donnees = json.load(f)
                
            for item in donnees:
                # Recherche ou création de la catégorie
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
            afficher_barre_notification(self.page_principale, f"{len(donnees)} notes importées avec succès !")
            journal.success(f"Importation terminée depuis {chemin_fichier}")
            
            # Rafraîchissement si possible (facultatif ici car on est dans paramètres)
        except Exception as ex:
            journal.error(f"Échec import JSON : {ex}")
            afficher_barre_notification(self.page_principale, "Fichier de sauvegarde invalide", est_erreur=True)

