import random
import cv2
import numpy as np

from utils import overlay_png


class SplitFruit:

    def __init__(self, image, x, y, side):

        self.image = image.copy()

        h, w = self.image.shape[:2]

        # Separate the halves with a small gap
        gap = 8

        if side == "left":
            self.image[:, w // 2 + gap:] = 0
            self.vx = random.uniform(-8, -5)
            self.rotation_speed = random.randint(-12, -6)
        else:
            self.image[:, :w // 2 - gap] = 0
            self.vx = random.uniform(5, 8)
            self.rotation_speed = random.randint(6, 12)

        self.x = x
        self.y = y

        self.vy = random.uniform(-12, -9)
        self.gravity = 0.45

        self.rotation = 0
        self.life = 65

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

        self.rotation += self.rotation_speed

        self.life -= 1

    def alive(self):
        return self.life > 0

    def draw(self, frame):

        h, w = self.image.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w // 2, h // 2),
            self.rotation,
            1.0
        )

        rotated = cv2.warpAffine(
            self.image,
            matrix,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_TRANSPARENT
        )

        x = int(self.x - w // 2)
        y = int(self.y - h // 2)

        overlay_png(frame, rotated, x, y)