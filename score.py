import cv2


class Score:

    def __init__(self):
        self.value = 0

    def add(self, points=1):
        self.value += points

    def draw(self, frame):

        cv2.putText(
            frame,
            f"Score: {self.value}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            f"Score: {self.value}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )