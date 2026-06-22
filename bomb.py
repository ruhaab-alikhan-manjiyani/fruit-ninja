from fruit import Fruit


class Bomb(Fruit):

    def __init__(self, width, height, image_paths):

        super().__init__(width, height, image_paths)

        self.name = "bomb"

        self.image = self.image