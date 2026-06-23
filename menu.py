import cv2


class Menu:

    def __init__(self):
        self.running = True

    def draw(self, frame):

        h, w = frame.shape[:2]

        # Dark transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.55, frame, 0.45, 0)

        # Title
        title = "FRUIT NINJA"

        size = cv2.getTextSize(
            title,
            cv2.FONT_HERSHEY_DUPLEX,
            2,
            4
        )[0]

        x = (w - size[0]) // 2

        cv2.putText(
            frame,
            title,
            (x, 180),
            cv2.FONT_HERSHEY_DUPLEX,
            2,
            (0, 0, 0),
            8
        )

        cv2.putText(
            frame,
            title,
            (x, 180),
            cv2.FONT_HERSHEY_DUPLEX,
            2,
            (0, 255, 255),
            4
        )

        # Subtitle
        cv2.putText(
            frame,
            "Move your index finger to slice fruits",
            (270, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        # Start instruction
        cv2.putText(
            frame,
            "Press SPACE to Start",
            (430, 430),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        # Quit instruction
        cv2.putText(
            frame,
            "Press ESC to Quit",
            (445, 485),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2
        )

        return frame