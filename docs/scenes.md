# Les scènes secondaires

Cette partie décrit les scènes secondaires du jeu qui permettent la navigation et la configuration en dehors de la scène principale `Jeu` (documentée dans `game.md`). Chaque scène est dérivée de la classe `Scene` du moteur et est implémentée dans son propre fichier. Elles sont conçues pour être simples et fonctionnelles.

## 1. Menu principal (`Menu`)

Le menu principal (définit dans `menu_main.py`) est le premier élément que voit le joueur. Il lui permet de jouer, d'accéder aux paramètres ou de quitter le jeu.

### Fonctionnement

Le Chargement (`load`) crée les éléments du menu : 
- Le logo (`tetr-art_logo_x4.png`) est affiché en haut. 
- Le fond avec un effet parallax (`bg_main.png`) est ajusté dynamiquement à la taille de l’écran. L'effet réagit au mouvement de la souris. Le parallax est mis à jour dans `update` avec `ease_in_out` pour un effet fluide. La position de la souris est enregistrée dans `mouse_pos` avec `handle_event`.
- Trois boutons centrés ("Jouer", "Paramètres", "Quitter") avec textures (`btn_main_normal.png`, `btn_main_hover.png`) et une police (`ChakraPetch-Bold.ttf`) permettent :
  - "Jouer" : Passe à `Selection_Menu`.
  - "Paramètres" : Passe à `Settings_Menu`.
  - "Quitter" : Définit `game.quit = True` pour fermer le jeu et arrêter la boucle principale.

Pour l'effet de parallax, l’image de fond, plus grande que l’écran, se déplace légèrement en sens inverse de la souris. La position est calculée avec `ease_in_out` (exposant 1.5) et une intensité `PARALLAX_INTENSITY = 15`, créant une illusion de profondeur.

## 2. Paramètres (`Settings_Menu`)

Le menu des paramètres (définit dans `menu_settings.py`) permet de personnaliser les touches de contrôle du jeu en modifiant les attributs de l'instance de `UserConfig` _\(comme mentionné [précédemment](engine.md#userconfig)\)_.
Le menu des paramètres permet aussi à l'utilisateur de modifier des réglages du jeu comme le volume ou la taille de l'interface.

Le Chargement (`load`) configure :
- Un titre "OPTIONS" en blanc (avec la police `ChakraPetch-Bold.ttf`).
- Une liste de touches configurables issue de `game.settings.inputs`, affichées avec leurs noms et boutons associés (avec la police `BaiJamjuree-Regular.ttf`).
- Un bouton "Retour" vers `Menu`.

### Système de binding :
- Lorsqu'on clique sur le bouton d'une touche, `ask_Bind` active le mode `isBinding`, affichant `><` sur le bouton de la touche. Le mode `isBinding` permet d'écouter les touches du clavier.
- Une pression de touche (`KEYDOWN`) remplace la commande dans `settings.inputs` et met à jour l’affichage avec un symbole unicode (ex. "←" pour "left") avec la méthode `get_unicode_from_keycode`.

## 3. Sélection des niveaux (`Selection_Menu`)

Le menu de sélection (`menu_selection.py`) permet de choisir un niveau à jouer, avec un pop-up indicatif sur l'œuvre sélectionnée.

Le Chargement (`load`) met en place :
- Un titre "JOUER" (`ChakraPetch-Bold.ttf`).
- Six boutons carrés pour les niveaux (Tutoriel + Niveaux 1-5) en grille 3x2, avec textures (`btn_selection_normal.png`, `btn_selection_hover.png`) et police `PressStart2P-Regular.ttf`.
- Un bouton "Retour" vers `Menu`.

Lorsqu'on clique sur un niveau (0 à 5), un pop-up s'ouvre et affiche des informations sur l'œuvre (le pop-up est une image). Deux boutons permettent :
- "Jouer" : Lance `Loading` avec l’ID du niveau.
- "X" : Ferme le pop-up avec `close_popup`.
Lorque le pop-up est ouvert, il désactive les boutons de sélection pendant son affichage pour éviter les conflits.

L'effet de parallax est identique à celui du menu principal.

