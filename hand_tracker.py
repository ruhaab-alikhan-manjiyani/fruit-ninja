import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    def __init__(self):
        model_path = "assets/models/hand_landmarker.task"

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2
        )

        self.detector = vision.HandLandmarker.create_from_options(options)
        self.trail = []
        self.last_tip = None
        self.speed = 0

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        return self.detector.detect(mp_image)

    def get_blade_tip(self, result, frame):
        if not result.hand_landmarks:
            self.last_tip = None
            self.speed = 0
            return None

        height, width = frame.shape[:2]

        hand = result.hand_landmarks[0]
        tip = hand[8]

        x = int(tip.x * width)
        y = int(tip.y * height)

        if self.last_tip is not None:
            dx = x - self.last_tip[0]
            dy = y - self.last_tip[1]

            self.speed = (dx * dx + dy * dy) ** 0.5

        self.last_tip = (x, y)

        return (x, y)

    def draw_landmarks(self, frame, result):
        if not result.hand_landmarks:
            return frame

        height, width = frame.shape[:2]

        connections = [
            (0,1),(1,2),(2,3),(3,4),
            (0,5),(5,6),(6,7),(7,8),
            (5,9),(9,10),(10,11),(11,12),
            (9,13),(13,14),(14,15),(15,16),
            (13,17),(17,18),(18,19),(19,20),
            (0,17)
        ]

        for hand in result.hand_landmarks:

            for start, end in connections:
                x1 = int(hand[start].x * width)
                y1 = int(hand[start].y * height)

                x2 = int(hand[end].x * width)
                y2 = int(hand[end].y * height)

                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            for i, landmark in enumerate(hand):
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                color = (0, 0, 255)

                if i == 8:
                    color = (255, 0, 0)

                cv2.circle(frame, (x, y), 6, color, -1)

        return frame

    def draw_blade(self, frame, result):
        if not result.hand_landmarks:
            self.trail.clear()
            return frame

        height, width = frame.shape[:2]

        hand = result.hand_landmarks[0]
        tip = hand[8]

        x = int(tip.x * width)
        y = int(tip.y * height)

        self.trail.append((x, y))

        if len(self.trail) > 8:
            self.trail.pop(0)

        for i in range(1, len(self.trail)):
            cv2.line(
                frame,
                self.trail[i - 1],
                self.trail[i],
                (255, 255, 0),
                5
            )

        return frame