# NoteApp 📝

## 📋 Description
NoteApp est une application de gestion de notes moderne, sécurisée et multi-plateforme développée avec Flet (Python). Elle permet de capturer des idées, d'organiser des catégories, de joindre des fichiers et de sécuriser les informations sensibles via le chiffrement.

## 🚀 Fonctionnalités
- ✍️ Édition de notes riche
- 📁 Organisation par catégories (chips)
- 🔒 Chiffrement des notes sensibles
- 🖇️ Gestion des pièces jointes
- 📄 Export PDF
- 🔔 Rappels intelligents
- 🌓 Mode Sombre / Clair (Design Cyber-Dark par défaut)

## 🛠️ Stack Technique
- **Langage** : Python 3.11+
- **Interface** : Flet (basé sur Flutter)
- **Base de données** : SQLite
- **Validation** : Pydantic
- **Sécurité** : Cryptography (Fernet)
- **Export** : FPDF2

## 📦 Prérequis
- Python 3.11 ou supérieur
- Un environnement virtuel configuré

## ⚙️ Installation
```bash
git clone https://github.com/BenSira99/NoteApp.git
cd NoteApp
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 🔧 Configuration (.env)
Créez un fichier `.env` à la racine pour les variables sensibles (ex: clé de chiffrement).

## 跑🏃 Lancement
```bash
flet run src/principal.py
```

## 🧪 Tests
```bash
pytest
```

## 📁 Structure du Projet
```text
NoteApp/
├── src/
│   ├── assets/       # Ressources statiques
│   ├── components/   # Composants UI réutilisables (en français)
│   ├── models/       # Modèles de données Pydantic/SQLite
│   ├── services/     # Logique métier (Auth, PDF, Chiffrement)
│   ├── utils/        # Constantes, Logging, Assistants
│   ├── views/        # Pages de l'application
│   └── principal.py  # Point d'entrée
├── tests/            # Tests unitaires
└── README.md
```

## 🔒 Sécurité
Toutes les notes marquées comme "sensibles" sont chiffrées avant le stockage en base de données.

## 📄 Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur — BenSira99
Développé avec rigueur et passion par Ben Sira.
