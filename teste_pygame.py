# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 11:04:11 2026

@author: paulo.goncalves
"""

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste Pygame")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()