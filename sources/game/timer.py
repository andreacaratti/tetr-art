#Projet : Tetr'Art
#Auteurs : Andrea CARATTI, Mohamad KARANOUH, Issam MOUTAWAKKIL, Raphael BRICAUD, Ulysse LEONARD SCHWARZ

class Timer():
    '''
    Initialize the time with the given duration.
    - duration (int): duration of the timer. If set to 0 or not defined
    - countdown (bool): Si True, le minuteur agit comme un compte à rebours. Sinon, c'est un chronomètre
    '''
    def __init__(self, duration=0, countdown=False):
        self.duration = duration
        self.elapsed = 0
        self.countdown = countdown
        self.active = False
        self.ended = False

    def update(self, dt):
        if not self.active:
            return
            #Retour anticipé, on ne mets pas à jour si non activé
        
        if self.countdown:
            # Lorsqu'il s'agit d'un minuteur
            if self.elapsed > 0 and self.ended == False:
                self.elapsed -= dt
            if self.elapsed <= 0:
                self.active = False
                self.ended = True
        else:
            # Lorsqu'il s'agit d'un chronomètre
            if (self.elapsed < self.duration or self.duration == 0) and self.ended == False:
                self.elapsed += dt
            if self.elapsed >= self.duration and self.duration != 0:
                self.active = False
                self.ended = True

    def reset(self):
        self.active = False
        self.ended = False
        if self.countdown:
            self.elapsed = self.duration
        else:
            self.elapsed = 0

    def stop(self):
        self.active = False

    def start(self):
        self.active = True
        if self.countdown:
            self.elapsed = self.duration
        else:
            self.elapsed = 0