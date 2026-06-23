import math
import random
import cv2

from fruit import Fruit
from bomb import Bomb
from heart import Heart
from particles import Particle
from split_fruit import SplitFruit
from sound import play_slice, play_bomb, play_gameover
from settings import FRUIT_SPAWN_TIME


class Game:

    def __init__(self):

        self.fruits = []
        self.particles = []
        self.split_fruits = []

        self.combo = 0
        self.combo_text = ""
        self.combo_text_timer = 0

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

        if self.game_over:
            return

        if self.combo_text_timer > 0:
            self.combo_text_timer -= 1

        self.spawn_timer += 1

        if self.spawn_timer >= FRUIT_SPAWN_TIME:

            self.spawn_timer = 0

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

        if self.game_over:
            return False

        if blade is None:
            return False

        if speed < 25:
            return False

        bx, by = blade

        sliced = False
        combo_hits = 0

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
                combo_hits += 1

                if fruit.name == "bomb":

                    play_bomb()

                    self.lives -= 1

                    if self.lives <= 0:
                        self.game_over = True
                        play_gameover()

                    continue

                play_slice()

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

        if combo_hits >= 2:

            if combo_hits == 2:
                self.combo_text = "DOUBLE!"

            elif combo_hits == 3:
                self.combo_text = "TRIPLE!"

            elif combo_hits == 4:
                self.combo_text = "AWESOME!"

            else:
                self.combo_text = "INSANE!"

            self.combo_text_timer = 40

        return sliced

    def draw(self, frame):

        # Particles
        for particle in self.particles:
            particle.draw(frame)

        # Split fruits
        for piece in self.split_fruits:
            piece.draw(frame)

        # Whole fruits
        for fruit in self.fruits:
            fruit.draw(frame)

        # Hearts
        frame_width = frame.shape[1]

        for i in range(self.lives):
            Heart(frame_width - 40 - i * 40, 40).draw(frame)

        # Combo text
        if self.combo_text_timer > 0:

            text_size = cv2.getTextSize(
                self.combo_text,
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                4
            )[0]

            x = (frame_width - text_size[0]) // 2

            cv2.putText(
                frame,
                self.combo_text,
                (x, 180),
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (0, 0, 0),
                8
            )

            cv2.putText(
                frame,
                self.combo_text,
                (x, 180),
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (0, 255, 255),
                4
            )

        # Game Over
        if self.game_over:

            text = "GAME OVER"

            size = cv2.getTextSize(
                text,
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                4
            )[0]

            x = (frame_width - size[0]) // 2
            y = frame.shape[0] // 2

            cv2.putText(
                frame,
                text,
                (x, y),
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (0, 0, 0),
                8
            )

            cv2.putText(
                frame,
                text,
                (x, y),
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (0, 0, 255),
                4
            )