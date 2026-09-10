import uuid

class Calque:
    def __init__(self, image):
        self.id = str(uuid.uuid4())
        self.image = image
        self.visible = True
        self.opacite = 100
        self.mode_fusion = "normal"
        self.nom = "Calque"