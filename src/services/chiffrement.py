"""
Service Chiffrement - Chiffrement AES-256-GCM pour les notes sensibles.
Utilise la bibliothèque cryptography avec dérivation de clé PBKDF2.
"""

import os
import base64
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.utils.journaliseur import journal

class ServiceChiffrement:
    """
    Service pour chiffrer et déchiffrer le contenu des notes en utilisant AES-256-GCM.
    """
    # Taille du sel en octets
    TAILLE_SEL = 16
    # Taille du nonce pour AES-GCM (12 octets recommandés)
    TAILLE_NONCE = 12
    # Taille de la clé pour AES-256 (32 octets)
    TAILLE_CLE = 32

    def __init__(self) -> None:
        self._cle_cachee: Optional[bytes] = None
        self._sel_cache: Optional[bytes] = None

    def deriver_cle(self, mot_de_passe: str, sel: bytes = None) -> Tuple[bytes, bytes]:
        """
        Dérive une clé de chiffrement à partir d'un mot de passe en utilisant PBKDF2.
        
        Args:
            mot_de_passe (str): Mot de passe ou PIN de l'utilisateur.
            sel (bytes): Sel optionnel (généré si non fourni).
            
        Returns:
            Tuple[bytes, bytes]: Le couple (clé, sel).
        """
        if sel is None:
            sel = os.urandom(self.TAILLE_SEL)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.TAILLE_CLE,
            salt=sel,
            iterations=100_000,
        )
        cle = kdf.derive(mot_de_passe.encode('utf-8'))
        return cle, sel

    def chiffrer(self, texte_clair: str, mot_de_passe: str) -> str:
        """
        Chiffre un texte clair en utilisant AES-256-GCM.
        
        Returns:
            str: Données chiffrées encodées en Base64 (sel + nonce + texte chiffré).
        """
        try:
            # Dérivation de la clé
            cle, sel = self.deriver_cle(mot_de_passe)
            # Génération du nonce
            nonce = os.urandom(self.TAILLE_NONCE)
            
            # Chiffrement
            aesgcm = AESGCM(cle)
            texte_chiffre = aesgcm.encrypt(nonce, texte_clair.encode('utf-8'), None)
            
            # Combinaison sel + nonce + texte chiffré et encodage
            donnees_combinees = sel + nonce + texte_chiffre
            encodage = base64.b64encode(donnees_combinees).decode('utf-8')
            
            journal.debug("Texte chiffré avec succès.")
            return encodage
        except Exception as e:
            journal.error(f"Erreur de chiffrement : {e}")
            raise ErreurChiffrement(f"Échec du chiffrement : {e}")

    def dechiffrer(self, donnees_chiffrees: str, mot_de_passe: str) -> str:
        """
        Déchiffre des données encodées en Base64.
        """
        try:
            # Décodage Base64
            donnees = base64.b64decode(donnees_chiffrees.encode('utf-8'))
            
            # Extraction du sel, du nonce et du contenu chiffré
            sel = donnees[:self.TAILLE_SEL]
            nonce = donnees[self.TAILLE_SEL:self.TAILLE_SEL + self.TAILLE_NONCE]
            contenu_chiffre = donnees[self.TAILLE_SEL + self.TAILLE_NONCE:]
            
            # Dérivation de la clé avec le même sel
            cle, _ = self.deriver_cle(mot_de_passe, sel)
            
            # Déchiffrement
            aesgcm = AESGCM(cle)
            texte_clair = aesgcm.decrypt(nonce, contenu_chiffre, None)
            
            journal.debug("Texte déchiffré avec succès.")
            return texte_clair.decode('utf-8')
        except Exception as e:
            journal.error(f"Erreur de déchiffrement : {e}")
            raise ErreurDechiffrement(f"Échec du déchiffrement : {e}")

class ErreurChiffrement(Exception):
    """Soulevée lorsque le chiffrement échoue."""
    pass

class ErreurDechiffrement(Exception):
    """Soulevée lorsque le déchiffrement échoue."""
    pass

# Instance singleton
_service_chiffrement: Optional[ServiceChiffrement] = None

def obtenir_service_chiffrement() -> ServiceChiffrement:
    """Retourne l'instance unique du service de chiffrement."""
    global _service_chiffrement
    if _service_chiffrement is None:
        _service_chiffrement = ServiceChiffrement()
    return _service_chiffrement
