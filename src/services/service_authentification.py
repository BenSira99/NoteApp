"""
Service Authentification - Gère la sécurité de l'application et l'authentification par PIN.
"""

import hashlib
from src.models.modele_parametres import ParametreApplication
from src.models.base_de_donnees import obtenir_session
from src.utils.journaliseur import journal

class ServiceAuthentification:
    """Service pour gérer l'authentification et la sécurité par code PIN."""
    
    def __init__(self) -> None:
        self.session = obtenir_session()

    def hacher_pin(self, pin: str) -> str:
        """Crée un hachage SHA-256 du code PIN."""
        return hashlib.sha256(pin.encode()).hexdigest()

    def verifier_pin(self, pin: str) -> bool:
        """Vérifie si le code PIN fourni correspond au hachage stocké."""
        try:
            hachage_stocke = ParametreApplication.obtenir_valeur(self.session, "hachage_pin")
            if not hachage_stocke:
                return False
            return self.hacher_pin(pin) == hachage_stocke
        except Exception as e:
            journal.error(f"Erreur lors de la vérification du PIN : {e}")
            return False

    def possede_pin(self) -> bool:
        """Vérifie si un code PIN est configuré et activé."""
        active = ParametreApplication.obtenir_valeur(self.session, "pin_active", "False") == "True"
        a_un_hachage = ParametreApplication.obtenir_valeur(self.session, "hachage_pin") is not None
        return active and a_un_hachage

    def definir_pin(self, pin: str) -> None:
        """Définit un nouveau code PIN."""
        hachage_pin = self.hacher_pin(pin)
        ParametreApplication.definir_valeur(self.session, "hachage_pin", hachage_pin)
        ParametreApplication.definir_valeur(self.session, "pin_active", "True")
        journal.info("Code PIN défini dans la base de données.")

    def supprimer_pin(self) -> None:
        """Supprime le code PIN et désactive la sécurité."""
        ParametreApplication.definir_valeur(self.session, "pin_active", "False")
        ParametreApplication.definir_valeur(self.session, "hachage_pin", "")
        journal.info("Code PIN supprimé de la base de données.")

# Instance globale
_service_authentification = ServiceAuthentification()

def obtenir_service_authentification() -> ServiceAuthentification:
    """Retourne l'instance unique du service d'authentification."""
    return _service_authentification
