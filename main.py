import cv2

from hand_tracker import HandTracker
from menu import Menu
from game import Game
from score import Score

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FPS, 60)

tracker = HandTracker()
game = Game()
score = Score()
menu = Menu()

started = False

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    height, width = frame.shape[:2]

    result = tracker.detect(frame)
    blade = tracker.get_blade_tip(result, frame)

    if not game.game_over:

        game.update(width, height)

        sliced = game.slice(blade, tracker.speed)

        if sliced:
            score.add()

    if not started:

        frame = menu.draw(frame)

        cv2.imshow("Fruit Ninja", frame)

        key = cv2.waitKey(1)

        if key == 32:      # SPACE
            started = True

        elif key == 27:    # ESC
            break

        continue

    # frame = tracker.draw_landmarks(frame, result)
    frame = tracker.draw_blade(frame, result)

    game.draw(frame)
    score.draw(frame)

    if game.game_over:
        cv2.putText(
            frame,
            "Press R to Restart",
            (380, 390),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2
        )[0]

    cv2.imshow("Fruit Ninja", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or key == 27:
        break

    if game.game_over and key == ord("r"):
        game = Game()
        score = Score()

camera.release()
cv2.destroyAllWindows()