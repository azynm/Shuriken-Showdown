import pygame
from pygame import *
#import bcrypt
import sqlite3
import sys
import random
from random import *
#the above imports the essential modules required
# * means import all
import screens
pygame.init()
import projectile
class character(pygame.sprite.Sprite):
    def __init__(self, health, positionx, positiony, speed): # constructor
        super().__init__()
        self.health = health  # integer for health
        self.positionx = positionx # initial x-coordinate
        self .positiony = positiony # initial y-coordinate
        self.speed = speed # rate of movement
        self.maxHealth = health # starting health
        self.remainingHealth = health # current health


class player(character):
    def __init__(self, health, positionx, positiony, speed):
        super().__init__(health, positionx, positiony, speed) # inheritance
        self.image = pygame.transform.scale(pygame.image.load('assets/NinjaGuy.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect() # gets rectangle around image
        self.rect.topleft = (positionx, positiony) # sets starting position

    def movePlayer(self):
            keystate = pygame.key.get_pressed() # gets state of all pressed keys as boolean value
            if keystate[pygame.K_w] and self.rect.y > 0:
                self.rect.y -= self.speed # up if w pressed
            if keystate[pygame.K_s] and self.rect.y < 1068:
                self.rect.y += self.speed # down if s pressed
            if keystate[pygame.K_a] and self.rect.x > 4:
                self.rect.x -= self.speed # left if a pressed
            if keystate[pygame.K_d] and self.rect.x < 1984:
                self.rect.x += self.speed # right if d pressed




class healthBar():
    def __init__(self, x, y, width, height, maxHP): # constructor
        self.x = x
        self.y = y # coordinates to draw
        self.barWidth = width
        self.barHeight = height
        self.maxhp = maxHP
        self.hp = maxHP #bar starts with max health

    def loadBar(self, surface):
         healthRatio = self.hp / self.maxhp # ratio used to determine how much the yellow bar decreases
         pygame.draw.rect(surface, 'red', (self.x, self.y, self.barWidth, self.barHeight))
         pygame.draw.rect(surface, 'yellow', (self.x, self.y, self.barWidth * healthRatio, self.barHeight)) # draw bars

class cyclops(character):
    def __init__(self, health, positionx, positiony, speed, cyclopsValue):
        super().__init__(health, positionx, positiony, speed) # inheritance
        self.image = pygame.transform.scale(pygame.image.load('assets/cyclops.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect() # gets image around rectangle
        self.rect.topleft = (positionx, positiony)
        self.speed = speed
        self.cyclopsValue = cyclopsValue

    def update(self, playerx, playery):
        # tracks player and moves towards them
        if self.rect.x < playerx:
            self.rect.x += self.speed # moves right
        if self.rect.x > playerx:
            self.rect.x -= self.speed # moves left
        if self.rect.y > playery:
            self.rect.y -= self.speed # moves up
        if self.rect.y < playery:
            self.rect.y += self.speed # moves down

        # checks if enemy should be dead
        if self.remainingHealth <=0:
            self.kill()


class dragon(character):
    def __init__(self, health, positionx, positiony, speed, dragonValue):
        super().__init__(health, positionx, positiony, speed)
        self.image = pygame.transform.scale(pygame.image.load('assets/dragon.png').convert_alpha(), (64, 64)) # scales image to 64x64
        self.rect = self.image.get_rect()
        self.rect.topleft = (positionx, positiony)
        self.speed = speed
        self.dragonValue = dragonValue

    def update(self, playerx, playery):
        # tracks player and moves towards them
        if self.rect.x < playerx:
            self.rect.x += self.speed
        if self.rect.x > playerx:
            self.rect.x -= self.speed
        if self.rect.y > playery:
            self.rect.y -= self.speed
        if self.rect.y < playery:
            self.rect.y += self.speed


        if self.remainingHealth <= 0:
                self.kill()


