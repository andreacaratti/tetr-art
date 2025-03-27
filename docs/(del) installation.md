# Installation et Exécution

## Prérequis
Avant d’installer et d’exécuter le jeu, assurez-vous d’avoir :

- **Python 3.13.0** installé sur votre machine. 
- **pip** (le gestionnaire de paquets Python).
- **Les bibliothèques nécessaires**, listées dans `requirements.txt`.

## Installation

1. **Cloner le dépôt du projet** (ou télécharger les fichiers) :

    ```sh
    git clone https://github.com/andreacaratti/nom-du-projet.git
    cd nom-du-projet
    ```

2. **Créer un environnement virtuel** (optionnel mais recommandé) :

   Sur macOS/Linux :
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

   Sur Windows :
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installer les dépendances** :

   ```sh
   pip install -r requirements.txt
   ```

## Exécution du jeu

Une fois l’installation terminée, vous pouvez lancer le jeu avec :
```sh
python sources\main.py
```

## Problèmes courants
Si vous rencontrez une erreur lors de l’installation ou de l’exécution, consultez [troubleshooting.md](troubleshooting.md)