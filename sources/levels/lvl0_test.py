#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

### NIVEAU DE TEST ###
from game.pieces import *
from game.level import *

SIZE_FACTOR = 0.3
IMG_RES = 3

class lvl0_test(level):
    def __init__(self):
        super().__init__()
        self.size = Vector2(10,15)

        self.total_pieces = 6
        self.pieces = [
            Piece(matrix=[[1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1]],
                id=1,
                correct_pos=Vector2(0,10)
                ),
            Piece(matrix=[[1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1]],
                id=2,
                correct_pos=Vector2(0,5)
                ),
            Piece(matrix=[[1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1]],
                id=3,
                correct_pos=Vector2(0,0)
                ),
            Piece(matrix=[[1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1]],
                id=4,
                correct_pos=Vector2(5,10)
                ),
            Piece(matrix=[[1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1]],
                id=5,
                correct_pos=Vector2(5,5)
                ),
            Piece(matrix=[[1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1],
                          [1,1,1,1,1]],
                id=6,
                correct_pos=Vector2(5,0)
                )
        ]

        self.SIZE_FACTOR = 0.3
        self.PIXELS_PER_TILE = 3

    def check(self, placed_pieces:list):
        count = 0
        remaining_pieces = len(self.pieces)
        for piece in placed_pieces:
            if piece.position == piece.correct_pos and piece.rotation == 0:
                count += 1
        return (count/(self.total_pieces+remaining_pieces)) if (self.total_pieces+remaining_pieces) > 0 else 0 
    
    def load_image(self):
        image = pygame.image.load("data/img/test/mona_lisa_test0.png").convert()
        self.split_image(image=image)