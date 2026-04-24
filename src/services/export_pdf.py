"""
Service Export PDF - Exporte les notes au format PDF.
Utilise ReportLab pour la génération de documents.
"""

import os
from datetime import datetime
from typing import List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from src.utils.journaliseur import journal
from src.utils.constantes import COULEUR_ACCENT, TITRE_APPLICATION

class ServiceExportPDF:
    """
    Service pour exporter les notes au format PDF.
    """
    # Marges de la page
    MARGE = 20 * mm

    def __init__(self, dossier_sortie: str = None) -> None:
        """
        Initialise le service d'exportation PDF.
        """
        if dossier_sortie is None:
            # Création du dossier exports s'il n'existe pas
            chemin_parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            dossier_sortie = os.path.join(chemin_parent, "exports")
            
        self.dossier_sortie = dossier_sortie
        os.makedirs(self.dossier_sortie, exist_ok=True)
        
        # Configuration des styles
        self._configurer_styles()

    def _configurer_styles(self) -> None:
        """Configure les styles de paragraphes pour le PDF."""
        self.styles = getSampleStyleSheet()
        
        # Style du titre
        self.styles.add(ParagraphStyle(
            name='TitreNote',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=10,
            textColor=colors.HexColor(COULEUR_ACCENT),
        ))
        
        # Style des métadonnées (date, catégorie)
        self.styles.add(ParagraphStyle(
            name='MetaNote',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=15,
        ))
        
        # Style du contenu
        self.styles.add(ParagraphStyle(
            name='ContenuNote',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            spaceAfter=20,
        ))

    def exporter_note(
        self,
        titre: str,
        contenu: str,
        categorie: str = None,
        date_creation: datetime = None,
        nom_fichier: str = None,
        chemin_complet: str = None,
    ) -> str:
        """
        Exporte une seule note en PDF.
        
        Returns:
            str: Le chemin vers le fichier PDF généré.
        """
        if chemin_complet is None:
            if nom_fichier is None:
                # Génération d'un nom de fichier sécurisé basé sur le titre
                titre_securise = "".join(c for c in titre if c.isalnum() or c in (' ', '-', '_'))[:50]
                horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
                nom_fichier = f"{titre_securise}_{horodatage}.pdf"
            chemin_complet = os.path.join(self.dossier_sortie, nom_fichier)

        try:
            doc = SimpleDocTemplate(
                chemin_complet,
                pagesize=A4,
                leftMargin=self.MARGE,
                rightMargin=self.MARGE,
                topMargin=self.MARGE,
                bottomMargin=self.MARGE,
            )

            # Construction du contenu du PDF
            elements = []
            
            # Titre
            elements.append(Paragraph(titre, self.styles['TitreNote']))
            
            # Métadonnées
            parties_meta = []
            if categorie:
                parties_meta.append(f"Catégorie: {categorie}")
            if date_creation:
                parties_meta.append(f"Créé le: {date_creation.strftime('%d/%m/%Y à %H:%M')}")
            
            if parties_meta:
                elements.append(Paragraph(" | ".join(parties_meta), self.styles['MetaNote']))
            
            # Contenu (remplacement des sauts de ligne)
            contenu_html = contenu.replace('\n', '<br/>')
            elements.append(Paragraph(contenu_html, self.styles['ContenuNote']))
            
            # Génération effective
            doc.build(elements)
            journal.info(f"PDF exporté avec succès : {chemin_complet}")
            return chemin_complet
            
        except Exception as e:
            journal.error(f"Erreur d'exportation PDF : {e}")
            raise ErreurExportPDF(f"Échec de l'exportation PDF : {e}")

class ErreurExportPDF(Exception):
    """Soulevée lorsque l'exportation PDF échoue."""
    pass

# Instance globale
_service_pdf: Optional[ServiceExportPDF] = None

def obtenir_service_pdf() -> ServiceExportPDF:
    """Retourne l'instance unique du service d'exportation PDF."""
    global _service_pdf
    if _service_pdf is None:
        _service_pdf = ServiceExportPDF()
    return _service_pdf
