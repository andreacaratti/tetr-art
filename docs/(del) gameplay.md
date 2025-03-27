# Gameplay

Le jeu est un puzzle basé sur des œuvres d’art célèbres. Chaque niveau représente une œuvre spécifique issue d’un mouvement artistique. L’objectif du joueur est de reconstituer l’image en plaçant correctement des pièces en forme de tétrominos sur une grille.

## Mécaniques principales

- Le joueur sélectionne et place les pièces manuellement sur la grille.
- Les pièces peuvent être déplacées avec la souris ou le clavier.
- Il est possible de faire pivoter une pièce avec la touche R ou un double-clic.
- La grille s’adapte à la difficulté choisie :
    - **Facile** &#8594; 10x10
    - **Moyen** &#8594; 16x16
    - **Difficile** &#8594; 20x20

## Chronomètre et Score

Chaque niveau est limité dans le temps. Le joueur doit compléter le puzzle avant la fin du minuteur.

Le score est calculé en fonction du nombre de pièces correctement placées :

$ \text{Score (\%)} = \frac{\text{Nombres de pièces bien placées}}{\text{Nombre total de pièce}} \times 100 $

Une fois le temps écoulé ou le puzzle terminé, le pourcentage de réussite s’affiche accompagné d'un message.

## Commandes

Les touches peuvent être configurées par le joueur dans le menu options. Les touches ar défaut sont :
- **Déplacement vers la gauche** : `A` ou flèche de gauche
- **Déplacement vers la droite** : `D` ou flèche de droite
- **Placer la pièce** : `S` ou flèche du bas
- **Rotation de la pièce** : `R` ou double click (moins de 500ms entre les clicks)

Le jeu est optimisé pour tourner à une fréquence fixe de 60 images par seconde, pour une expérience fluide.