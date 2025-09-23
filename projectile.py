import pygame
from pygame import *
#import bcrypt
import sqlite3
import sys
import random
from random import *
#the above imports the essential modules required
# * means import all
pygame.init()

class projectile(pygame.sprite.Sprite):
    def __init__(self, positionx, positiony, speed, damage): # constructor
        super().__init__()
        self.positionx = positionx
        self.positiony = positiony
        self.speed = speed #controls how fast bullet moves
        self.damage = damage


class shuriken(projectile):
    def __init__(self, positionx, positiony, speed, damage):
        super().__init__(positionx, positiony, speed, damage)
        self.image = pygame.transform.scale(pygame.image.load('assets/shuriken.png'), (64, 64)) # makes image 64x64
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony) # spawn position

class yshuriken(shuriken): # vertical shuriken
    def __init__(self, positionx, positiony, speed, damage):
        super().__init__(positionx, positiony, speed, damage)
        self.image = pygame.transform.scale(pygame.image.load('assets/shuriken.png'), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony) # spawn position
        self.launchTime = pygame.time.get_ticks() # time of launch

    def update(self):
        currentTime = pygame.time.get_ticks()
        if (currentTime - self.launchTime) <= 800:  # move for 0.8 seconds
            self.rect.y += self.speed  # move shuriken
        else:
            self.kill()

class xshuriken(shuriken): # horizontal shuriken
    def __init__(self, positionx, positiony, speed, damage):
        super().__init__(positionx, positiony, speed, damage)
        self.image = pygame.transform.scale(pygame.image.load('assets/shuriken.png'), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony) # spawn position
        self.startTime = pygame.time.get_ticks() # time of launch

    def update(self):
        currentTime = pygame.time.get_ticks()
        if (currentTime - self.startTime) <= 800: # move for 0.8 seconds
            self.rect.x += self.speed # move shuriken
        else:
            self.kill()

class fireball(projectile):
    def __init__(self, positionx, positiony, speed, damage):
        super().__init__(positionx, positiony, speed, damage) # inherits from superclass
        self.image = pygame.transform.scale(pygame.image.load('assets/fireball.png'), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony) # spawn position

class xfireball(fireball):
    def __init__(self, positionx, positiony, speed, damage):
        super().__init__(positionx, positiony, speed, damage) # inherits from superclass
        self.image = pygame.transform.scale(pygame.image.load('assets/fireball.png'), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony) # spawn position
        self.startTime = pygame.time.get_ticks() # time of launch

    def update(self):
        currentTime = pygame.time.get_ticks() # starts a timer
        if (currentTime - self.startTime) <= 1000: # moves for 1 second
            self.rect.x += self.speed # horizontal movement
        else:
            self.kill() # de-spawns

class yfireball(fireball):
    def __init__(self, positionx, positiony, speed, damage):
        super().__init__(positionx, positiony, speed, damage) # inherits from superclass
        self.image = pygame.transform.scale(pygame.image.load('assets/fireball.png'), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony) # spawn position
        self.startTime = pygame.time.get_ticks() # time of launch

    def update(self):
        currentTime = pygame.time.get_ticks() # starts a timer
        if (currentTime - self.startTime) <= 1000: # moves for 1 second
            self.rect.y += self.speed # vertical movement
        else:
            self.kill() # de-spawns
