"""
VueAccueil - Écran principal affichant la liste des notes.
"""

import flet as ft
from src.models.note import Note
from src.models.categorie import Categorie
from src.models.base_de_donnees import obtenir_session
from src.components.carte_note import CarteNote
from src.components.barre_recherche import BarreRecherche
from src.components.puce_categorie import PuceCategorie
from src.utils.constantes import Couleurs, ConfigurationApp
from src.utils.journaliseur import journal

class VueAccueil(ft.Container):
    """
    Écran d'accueil présentant les notes avec recherche et filtrage.
    """
    FILTRE_FAVORIS = "favoris"

    def __init__(self, page: ft.Page, sur_clic_note=None) -> None:
        super().__init__()
        self.page_principale = page
        self.sur_clic_note = sur_clic_note
        self._filtre_actuel = None  # ID de catégorie ou FILTRE_FAVORIS
        self._requete_recherche = ""
        self.session_db = obtenir_session()

        # Barre de recherche
        self.barre_recherche = BarreRecherche(
            "Rechercher une note...",
            sur_changement=self._sur_changement_recherche
        )

        # Ligne de filtres de catégories
        self.ligne_categories = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
        )

        # Liste des notes
        self.liste_notes = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.symmetric(horizontal=16),
        )

        # État vide
        self.etat_vide = ft.Column(
            [
                ft.Icon(ft.Icons.NOTE_ADD_ROUNDED, size=100, color=ft.Colors.GREY_800),
                ft.Text("Aucune note trouvée", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Commencez par créer votre première idée !", color=ft.Colors.GREY_400),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        # Conteneur principal de contenu (centré pour l'état vide)
        self.conteneur_contenu = ft.Container(expand=True, alignment=ft.Alignment(0, 0))

        self.content = ft.Column(
            [
                self.barre_recherche,
                ft.Container(self.ligne_categories, padding=ft.padding.symmetric(horizontal=16)),
                self.conteneur_contenu,
            ],
            expand=True,
        )
        self.expand = True

        self.rafraichir()

    def rafraichir(self) -> None:
        """Rafraîchit la liste des notes et des filtres."""
        self._charger_filtres()
        self._charger_notes()

    def _charger_filtres(self) -> None:
        """Charge les puces de filtrage."""
        self.ligne_categories.controls.clear()
        
        # Puce "Toutes"
        self.ligne_categories.controls.append(
            PuceCategorie(
                "Toutes",
                sur_clic=lambda _: self._filtrer_par_categorie(None),
                selectionnee=self._filtre_actuel is None
            )
        )
        
        # Puce "Favoris"
        self.ligne_categories.controls.append(
            PuceCategorie(
                "Favoris",
                couleur=ft.Colors.AMBER_600,
                sur_clic=lambda _: self._filtrer_par_categorie(self.FILTRE_FAVORIS),
                selectionnee=self._filtre_actuel == self.FILTRE_FAVORIS
            )
        )
        
        # Puces des catégories réelles
        categories = self.session_db.query(Categorie).all()
        for cat in categories:
            self.ligne_categories.controls.append(
                PuceCategorie(
                    cat.nom,
                    couleur=cat.couleur,
                    sur_clic=lambda _, c_id=cat.identifiant: self._filtrer_par_categorie(c_id),
                    selectionnee=self._filtre_actuel == cat.identifiant
                )
            )
        
        try: self.ligne_categories.update()
        except: pass

    def _charger_notes(self) -> None:
        """Charge les notes en fonction des filtres actifs."""
        self.liste_notes.controls.clear()
        requete = self.session_db.query(Note)

        # Application du filtre de catégorie / favoris
        if self._filtre_actuel == self.FILTRE_FAVORIS:
            requete = requete.filter(Note.est_favoris == True)
        elif self._filtre_actuel:
            requete = requete.filter(Note.id_categorie == self._filtre_actuel)

        # Application de la recherche
        if self._requete_recherche:
            requete = requete.filter(
                (Note.titre.ilike(f"%{self._requete_recherche}%")) |
                (Note.contenu.ilike(f"%{self._requete_recherche}%"))
            )

        # Tri par date de modification
        notes = requete.order_by(Note.date_modification.desc()).all()

        if notes:
            self.conteneur_contenu.content = self.liste_notes
            for n in notes:
                carte = CarteNote(
                    id_note=n.identifiant,
                    titre=n.titre,
                    aperçu=n.obtenir_aperçu(),
                    nom_categorie=n.categorie.nom if n.categorie else None,
                    couleur_categorie=n.categorie.couleur if n.categorie else None,
                    est_favoris=n.est_favoris,
                    est_chiffree=n.est_chiffree,
                    date_mise_a_jour=n.date_modification,
                    sur_clic=self._gerer_clic_note,
                    sur_clic_favori=self._gerer_clic_favori
                )
                self.liste_notes.controls.append(carte)
        else:
            self.conteneur_contenu.content = self.etat_vide

        try: self.conteneur_contenu.update()
        except: pass

    def _sur_changement_recherche(self, requete: str) -> None:
        """Gère la saisie dans la barre de recherche."""
        self._requete_recherche = requete
        self._charger_notes()

    def _filtrer_par_categorie(self, id_cat) -> None:
        """Filtre les notes par catégorie."""
        self._filtre_actuel = id_cat
        self._charger_filtres()
        self._charger_notes()

    def _gerer_clic_note(self, id_note: int) -> None:
        """Redirige vers l'éditeur pour la note sélectionnée."""
        journal.info(f"Note sélectionnée : {id_note}")
        # La navigation est gérée par le chef d'orchestre dans app.py
        # Appel via une éventuelle fonction de rappel ou via la page
        from src.app import ApplicationNote
        page_app = getattr(self.page_principale, "app_instance", None)
        if page_app:
            page_app._naviguer_vers_editeur(id_note)

    def _gerer_clic_favori(self, id_note: int) -> None:
        """Bascule l'état favori d'une note."""
        try:
            note = self.session_db.query(Note).filter(Note.id == id_note).first()
            if note:
                note.est_favoris = not note.est_favoris
                self.session_db.commit()
                self._charger_notes()
        except Exception as e:
            journal.error(f"Erreur favori : {e}")
