import json
import os

FILE_NAME = "highscore.json"


def load_highscore():

    if not os.path.exists(FILE_NAME):
        return 0

    with open(FILE_NAME, "r") as file:
        data = json.load(file)

    return data.get("highscore", 0)


def save_highscore(score):

    with open(FILE_NAME, "w") as file:
        json.dump(
            {"highscore": score},
            file,
            indent=4
        )