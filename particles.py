import random
import cv2


class Particle:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-8, 8)

        self.radius = random.randint(3, 7)

        self.life = 30

        self.color = color

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.3

        self.life -= 1

    def draw(self, frame):

        if self.life <= 0:
            return

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            self.radius,
            self.color,
            -1
        )

    def alive(self):
        return self.life > 0