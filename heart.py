import cv2


class Heart:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, frame):

        cv2.circle(frame, (self.x - 8, self.y), 8, (0, 0, 255), -1)
        cv2.circle(frame, (self.x + 8, self.y), 8, (0, 0, 255), -1)

        points = [
            (self.x - 16, self.y),
            (self.x + 16, self.y),
            (self.x, self.y + 22)
        ]

        cv2.fillPoly(frame, [__import__("numpy").array(points)], (0, 0, 255))