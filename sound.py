import pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.init()

slice_sound = pygame.mixer.Sound("assets/sounds/slice.wav")
bomb_sound = pygame.mixer.Sound("assets/sounds/bomb.wav")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")


def play_slice():
    slice_sound.play()


def play_bomb():
    bomb_sound.play()


def play_gameover():
    gameover_sound.play()