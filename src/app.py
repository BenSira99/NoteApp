"""
NoteApp - Une application de prise de notes sécurisée construite avec Flet.
Point d'entrée principal avec navigation entre les vues.
"""

import flet as ft
from src.models.base_de_donnees import initialiser_base_de_donnees
from src.models.note import Note
from src.models.categorie import Categorie
from src.views.accueil import VueAccueil
from src.views.editeur import VueEditeur
from src.views.parametres import VueParametres
from src.views.categories import VueCategories
from src.utils.journaliseur import journal
from src.utils.constantes import COULEUR_ACCENT, COULEUR_SECONDAIRE, COULEUR_DANGER, TITRE_APPLICATION
from src.services.service_authentification import obtenir_service_authentification

class ApplicationNote:
    """
    Classe principale de l'application gérant la navigation et l'état.
    """
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self._vue_actuelle = None
        self._configurer_page()
        self._initialiser_donnees()
        
        # Enregistrement de l'instance pour la navigation
        self.page.app_instance = self
        
        # Vérification de la protection par PIN
        self._verifier_authentification()

    def _verifier_authentification(self) -> None:
        """Vérifie la présence d'un PIN et affiche l'écran de verrouillage ou l'accueil."""
        authentification = obtenir_service_authentification()
        if authentification.possede_pin():
            self._afficher_ecran_verrouillage()
        else:
            self._naviguer_vers_accueil()

    def _afficher_ecran_verrouillage(self) -> None:
        """Affiche l'écran de verrouillage par PIN."""
        authentification = obtenir_service_authentification()
        journal.info("Affichage de l'écran de verrouillage.")
        
        champ_pin = ft.TextField(
            label="Entrez votre PIN",
            password=True,
            can_reveal_password=True,
            text_align=ft.TextAlign.CENTER,
            width=250,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=6,
            on_submit=lambda _: verifier_le_pin(None),
            autofocus=True,
            border_color=COULEUR_ACCENT
        )
        
        texte_erreur = ft.Text("", color=COULEUR_DANGER, size=12, visible=False)

        def verifier_le_pin(e: ft.ControlEvent) -> None:
            pin = champ_pin.value
            if authentification.verifier_pin(pin):
                self._naviguer_vers_accueil()
            else:
                champ_pin.value = ""
                texte_erreur.value = "Code PIN incorrect"
                texte_erreur.visible = True
                self.page.update()

        vue_verrouillage = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_PERSON, size=80, color=COULEUR_ACCENT),
                    ft.Text(TITRE_APPLICATION, size=28, weight=ft.FontWeight.BOLD),
                    ft.Container(height=20),
                    champ_pin,
                    texte_erreur,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Déverrouiller", 
                        on_click=verifier_le_pin,
                        bgcolor=COULEUR_ACCENT,
                        color=ft.Colors.WHITE
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            expand=True,
            bgcolor=ft.Colors.SURFACE,
        )
        
        self.page.controls.clear()
        self.page.add(vue_verrouillage)
        self.page.update()

    def _configurer_page(self) -> None:
        """Configure les paramètres globaux de la page Flet."""
        self.page.title = TITRE_APPLICATION
        self.page.theme_mode = ft.ThemeMode.DARK  # Priorité au mode sombre Luxury
        self.page.padding = 0
        
        # Thème Personnalisé
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=COULEUR_ACCENT,
                secondary=COULEUR_SECONDAIRE,
                error=COULEUR_DANGER,
                surface=ft.Colors.BLACK,
            )
        )
    
    def _initialiser_donnees(self) -> None:
        """Initialise la base de données et les données par défaut."""
        journal.info("Préparation de la base de données...")
        session = initialiser_base_de_donnees()
        Categorie.creer_par_defaut(session)
        journal.info("Base de données prête.")

    def _naviguer_vers_accueil(self) -> None:
        """Navigue vers la vue d'accueil."""
        journal.info("Navigation vers l'Accueil")
        vue_accueil = VueAccueil(self.page)
        
        # Configuration de l'AppBar
        self.page.appbar = ft.AppBar(
            title=ft.Text(TITRE_APPLICATION, weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.CATEGORY,
                    tooltip="Catégories",
                    on_click=lambda _: self._naviguer_vers_categories(),
                ),
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    tooltip="Paramètres",
                    on_click=lambda _: self._naviguer_vers_parametres(),
                ),
            ],
        )
        
        # Bouton d'action flottant (FAB)
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=COULEUR_ACCENT,
            on_click=lambda _: self._naviguer_vers_editeur(),
        )
        
        self._definir_vue(vue_accueil)

    def _naviguer_vers_parametres(self) -> None:
        """Navigue vers la vue des paramètres."""
        journal.info("Navigation vers les Paramètres")
        vue_parametres = VueParametres(self.page)
        
        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: self._naviguer_vers_accueil(),
            ),
            title=ft.Text("Paramètres", weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )
        
        self.page.floating_action_button = None
        self._definir_vue(vue_parametres)

    def _naviguer_vers_categories(self) -> None:
        """Navigue vers la gestion des catégories."""
        journal.info("Navigation vers les Catégories")
        vue_categories = VueCategories(self.page)
        
        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: self._naviguer_vers_accueil(),
            ),
            title=ft.Text("Catégories", weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )
        
        self.page.floating_action_button = None
        self._definir_vue(vue_categories)

    def _naviguer_vers_editeur(self, id_note: int = None) -> None:
        """Navigue vers l'éditeur de notes."""
        est_nouvelle = id_note is None
        journal.info(f"Navigation vers l'Éditeur (Nouvelle={est_nouvelle}, ID={id_note})")
        
        vue_editeur = VueEditeur(self.page, id_note=id_note)
        
        def action_sauvegarder(e):
            if vue_editeur.sauvegarder():
                self._naviguer_vers_accueil()

        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=lambda _: self._naviguer_vers_accueil(),
            ),
            title=ft.Text(
                "Nouvelle Note" if est_nouvelle else "Modifier la Note",
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SAVE,
                    tooltip="Enregistrer",
                    on_click=action_sauvegarder
                ),
            ],
        )
        
        self.page.floating_action_button = None
        self._definir_vue(vue_editeur)

    def _definir_vue(self, vue: ft.View) -> None:
        """Définit la vue actuelle et met à jour la page."""
        self._vue_actuelle = vue
        self.page.controls.clear()
        self.page.add(ft.SafeArea(vue, expand=True))
        self.page.update()

def principal(page: ft.Page) -> None:
    """Point d'entrée principal de l'application Flet."""
    # Configuration de l'icône
    page.window_icon = "NoteApp.png"
    journal.info("Démarrage de NoteApp...")
    
    # Lancement de l'application (Plus de FilePicker Flet instable)
    ApplicationNote(page)
    page.update()

if __name__ == "__main__":
    # Lancement de l'application avec spécification du dossier des ressources
    ft.app(principal, assets_dir="src/assets")
