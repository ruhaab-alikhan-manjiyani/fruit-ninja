import random
import cv2
from utils import overlay_png


class SplitFruit:

    def __init__(self, image, x, y, side):

        self.image = image.copy()

        h, w = self.image.shape[:2]

        if side == "left":
            self.image[:, w // 2:] = 0
        else:
            self.image[:, :w // 2] = 0

        self.x = x
        self.y = y

        self.side = side

        if side == "left":
            self.vx = -6
            self.angle = -25
        else:
            self.vx = 6
            self.angle = 25

        self.vy = -8
        self.gravity = 0.4

        self.rotation = 0
        self.rotation_speed = random.randint(-8, 8)

        self.life = 60

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
           1
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