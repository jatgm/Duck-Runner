import pygame, sys, os
import random

pygame.init()
clock = pygame.time.Clock()

screen_height = 786
screen_width = 1024

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Duck Runner')