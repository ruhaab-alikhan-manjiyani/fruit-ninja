import cv2
import random

from settings import GRAVITY
from utils import overlay_png


class Fruit:

    def __init__(self, width, height, image_paths):
        self.name = random.choice(list(image_paths.keys()))
        path = image_paths[self.name]

        self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if self.image is None:
            raise FileNotFoundError(f"Could not load image: {path}")

        self.image = cv2.resize(self.image, (120, 120))
        self.radius = 55

        self.x = random.randint(120, width - 120)
        self.y = height + 100

        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-26, -22)

        self.gravity = GRAVITY
        self.radius = 45
        self.alive = True
        self.sliced = False

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

    def draw(self, frame):

        h, w = self.image.shape[:2]

        x = int(self.x - w // 2)
        y = int(self.y - h // 2)

        overlay_png(frame, self.image, x, y)

    def off_screen(self, height):

        return self.y > height + 120