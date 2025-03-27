#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

def rotate_matrix(matrix):
    return list(zip(*matrix[::-1]))

# Liste des formes. Peuvent être orientées.
pieces_list = {
    "I" : [[1],[1],[1],[1]],

    "O" : [[1,1],
           [1,1]],

    "T" : [[1,1,1],
           [None,1,None]],
    
    "L" : [[1,1,1],
           [1,None,None]],

    "J" : [[1,1,1],
           [None,None,1]],

    "Z" : [[1,1,None],
           [None,1,1]],

    "S" : [[None,1,1],
           [1,1,None]],
}