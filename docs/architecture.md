# Architecture du projet
Le projet est structuré en plusieurs dossiers et fichiers pour assurer une bonne organisation et une séparation claire des responsabilités.

## Arborescence du projet
```sh
TETRART
├── data/           # Ressources (images, sons, polices)
│   ├── fonts/          
│   ├── sounds/         
│   └── img/            
├── sources/        # Code source du projet
│   ├── ui/             
│   ├── game/           
│   ├── engine/         
│   ├── scenes/         
│   ├── levels/         
│   ├── constants.py    
│   ├── config.py       
│   └── main.py         
├── docs/           # Documentation technique
```

## Description des dossiers et fichiers dans `sources/`
- `main.py` : Initialise le moteur.

- `engine/` : Contient le moteur de jeu qui gère la boucle principale, les mises à jour de la logique et l'affichage avec pygame et la gestion des évènements. Définit les classes principales comme `Scene`.

- `scenes/` : Contient les différentes scènes du jeu (menu principal, niveau, menu réglage, menu de selection des niveaux).

- `game/` : Contient les mécaniques du jeu (gestion des pièces, grille de jeu et placement).

- `levels/` : Contient les différents niveaux comme des classes dérivées de `Level`.

- `config.py` : donne le chemin de base de l'application.

- `constants.py` : Contient les constantes du jeu.