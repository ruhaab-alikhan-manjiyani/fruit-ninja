import math
import random

from fruit import Fruit
from heart import Heart
from bomb import Bomb
from particles import Particle
from split_fruit import SplitFruit
from settings import FRUIT_SPAWN_TIME


class Game:

    def __init__(self):

        self.fruits = []
        self.particles = []
        self.split_fruits = []

        self.spawn_timer = 0

        self.lives = 3
        self.game_over = False

        self.image_paths = {
            "apple": "assets/fruits/apple.png",
            "banana": "assets/fruits/banana.png",
            "bomb": "assets/fruits/bomb.png",
            "grapes": "assets/fruits/grapes.png",
            "greenapple": "assets/fruits/greenapple.png",
            "orange": "assets/fruits/orange.png",
            "pineapple": "assets/fruits/pineapple.png",
            "pomegranate": "assets/fruits/pomegranate.png",
            "strawberry": "assets/fruits/strawberry.png",
            "watermelon": "assets/fruits/watermelon.png"
        }

        self.colors = {
            "apple": (0, 0, 255),
            "banana": (0, 255, 255),
            "bomb": (40, 40, 40),
            "grapes": (180, 0, 180),
            "greenapple": (0, 255, 0),
            "orange": (0, 165, 255),
            "pineapple": (0, 255, 255),
            "pomegranate": (30, 30, 220),
            "strawberry": (0, 0, 200),
            "watermelon": (80, 0, 255)
        }

    def update(self, width, height):

        self.spawn_timer += 1

        if self.spawn_timer >= FRUIT_SPAWN_TIME:

            self.spawn_timer = 0

            # 1 bomb out of every 6 spawns
            count = random.randint(2, 5)

            for _ in range(count):

                if random.randint(1, 8) == 1:
                   self.fruits.append(
                      Bomb(width, height, self.image_paths)
     )
                else:
                   self.fruits.append(
                      Fruit(width, height, self.image_paths)
        )

        for fruit in self.fruits:
            fruit.update()

        for particle in self.particles:
            particle.update()

        for piece in self.split_fruits:
            piece.update()

        self.fruits = [
            fruit for fruit in self.fruits
            if fruit.alive and not fruit.off_screen(height)
        ]

        self.particles = [
            particle for particle in self.particles
            if particle.alive()
        ]

        self.split_fruits = [
            piece for piece in self.split_fruits
            if piece.alive()
        ]

    def slice(self, blade, speed):

        if blade is None:
            return False

        if speed < 25:
            return False

        bx, by = blade
        sliced = False

        for fruit in self.fruits:

            distance = math.sqrt(
                (fruit.x - bx) ** 2 +
                (fruit.y - by) ** 2
            )

            if (
                distance <= fruit.radius
                and fruit.alive
                and not fruit.sliced
            ):

                fruit.sliced = True
                fruit.alive = False
                sliced = True

                if fruit.name == "bomb":
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    continue

                self.split_fruits.append(
                    SplitFruit(
                        fruit.image,
                        fruit.x,
                        fruit.y,
                        "left"
                    )
                )

                self.split_fruits.append(
                    SplitFruit(
                        fruit.image,
                        fruit.x,
                        fruit.y,
                        "right"
                    )
                )

                color = self.colors.get(
                    fruit.name,
                    (255, 255, 255)
                )

                for _ in range(35):
                    self.particles.append(
                        Particle(
                            fruit.x,
                            fruit.y,
                            color
                        )
                    )

        return sliced

    def draw(self, frame):

        for particle in self.particles:
           particle.draw(frame)

        for piece in self.split_fruits:
           piece.draw(frame)

        for fruit in self.fruits:
           fruit.draw(frame)

        for i in range(self.lives):
            Heart(40 + i * 35, 40).draw(frame)