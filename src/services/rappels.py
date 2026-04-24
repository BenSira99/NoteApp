"""
Service Rappels - Gère les rappels et les notifications liés aux notes.
Utilise python-dateutil pour la manipulation flexible des dates.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from src.utils.journaliseur import journal

class ServiceRappels:
    """
    Service pour gérer les rappels des notes.
    """
    def __init__(self) -> None:
        self._rappels_programmes = {}

    def analyser_date(self, chaine_date: str) -> Optional[datetime]:
        """
        Analyse une chaîne de caractères en objet datetime.
        """
        try:
            return date_parser.parse(chaine_date, dayfirst=True)
        except Exception as e:
            journal.warning(f"Échec de l'analyse de la date '{chaine_date}' : {e}")
            return None

    def obtenir_heure_rappel_par_defaut(self, date_entree: datetime = None) -> datetime:
        """
        Retourne l'heure de rappel par défaut (aujourd'hui à 09:00 par défaut).
        """
        if date_entree is None:
            date_entree = datetime.now()
        return date_entree.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0,
        )

    def obtenir_rappels_a_venir(self, notes_avec_rappels: List[dict], jours_horizon: int = 7) -> List[dict]:
        """
        Récupère les notes dont le rappel arrive bientôt.
        """
        maintenant = datetime.now()
        date_limite = maintenant + timedelta(days=jours_horizon)
        a_venir = []
        
        for note in notes_avec_rappels:
            date_rappel = note.get('date_rappel')
            if date_rappel and maintenant <= date_rappel <= date_limite:
                a_venir.append(note)
        
        # Tri par date de rappel
        a_venir.sort(key=lambda n: n['date_rappel'])
        return a_venir

    def formater_date_rappel(self, date_rappel: datetime) -> str:
        """
        Formate une date de rappel pour un affichage convivial.
        """
        maintenant = datetime.now()
        if date_rappel.date() == maintenant.date():
            return f"Aujourd'hui à {date_rappel.strftime('%H:%M')}"
        elif date_rappel.date() == (maintenant + timedelta(days=1)).date():
            return f"Demain à {date_rappel.strftime('%H:%M')}"
        elif date_rappel.date() == (maintenant - timedelta(days=1)).date():
            return f"Hier à {date_rappel.strftime('%H:%M')}"
        elif date_rappel.year == maintenant.year:
            return date_rappel.strftime("%d %b à %H:%M")
        else:
            return date_rappel.strftime("%d/%m/%Y à %H:%M")

    def programmer_rappel(self, id_note: int, date_rappel: datetime) -> bool:
        """
        Programme un rappel pour une note.
        Note : Placeholder pour une intégration future avec les notifications système.
        """
        try:
            self._rappels_programmes[id_note] = date_rappel
            journal.info(f"Rappel programmé pour la note {id_note} à {date_rappel}")
            return True
        except Exception as e:
            journal.error(f"Échec de la programmation du rappel : {e}")
            return False

    def annuler_rappel(self, id_note: int) -> bool:
        """
        Annule un rappel programmé.
        """
        if id_note in self._rappels_programmes:
            del self._rappels_programmes[id_note]
            journal.info(f"Rappel annulé pour la note {id_note}")
            return True
        return False

# Instance globale
_service_rappels: Optional[ServiceRappels] = None

def obtenir_service_rappels() -> ServiceRappels:
    """Retourne l'instance unique du service de rappels."""
    global _service_rappels
    if _service_rappels is None:
        _service_rappels = ServiceRappels()
    return _service_rappels
