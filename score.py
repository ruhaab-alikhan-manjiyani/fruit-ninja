import cv2

from highscore import load_highscore, save_highscore


class Score:

    def __init__(self):

        self.value = 0
        self.highscore = load_highscore()

    def add(self, points=1):

        self.value += points

        if self.value > self.highscore:
            self.highscore = self.value
            save_highscore(self.highscore)

    def reset(self):

        self.value = 0

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

        cv2.putText(
            frame,
            f"Best: {self.highscore}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            f"Best: {self.highscore}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (100, 215, 255),
            2
        )