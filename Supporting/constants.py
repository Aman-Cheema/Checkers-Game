import pygame

# RGB
black = (  0,  0,  0)
white = (255,255,255)
marron  = (127, 28, 28)
Khaki = (240,230,140)

# Dimentions
Width, Height = 800, 800
Rows, Cols = 8, 8

# Image of Crown
Crown = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

# Background
Background = pygame.transform.scale(pygame.image.load('assets/Wooden_Background.jpg'), (800, 800))