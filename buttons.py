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
clock = pygame.time.Clock()
fps = 60 #sets the frame rate for the screens

class Button(pygame.sprite.Sprite): #class for pygame sprites
    def __init__(self, x, y,): #x and y coordinates
        super().__init__()
        self.x = x
        self.y = y

class SignInButton(Button): #inherits from button class
    def __init__(self, x, y):
        super().__init__( x, y)
        signInWidth = 300
        signInHeight = 150
        #sets dimensions
        self.signInImage = pygame.Surface((signInWidth, signInHeight))
        self.signInImage.fill((173, 216, 230)) #light blue colouring
        signInFont = pygame.font.Font(None, 26) #sets font to default and size 26
        signInText = signInFont.render("SIGN-IN", True, (0, 0, 0)) #loads in string in black colour
        signInTextRect = signInText.get_rect(center=(signInWidth // 2, signInHeight // 2)) #centers text
        self.signInImage.blit(signInText, signInTextRect) #draws text onto surface
        self.signInRect = self.signInImage.get_rect() #gets rectangle around button
        self.signInRect.topleft = (x, y)

    def loadSigninButton(self, surface):
        surface.blit(self.signInImage, (self.signInRect.x, self.signInRect.y)) #loads button onto screen®

class RegistrationButton(Button):  # inherits from button class
    def __init__(self, x, y):
        super().__init__(x, y)
        registerWidth = 300
        registerHeight = 150
        #sets dimensions
        self.registerImage = pygame.Surface((registerWidth, registerHeight))
        self.registerImage.fill((173, 216, 230))  # light blue colouring
        registerFont = pygame.font.Font(None, 26)  # sets font to default and size 26
        registerText = registerFont.render("REGISTER", True, (0, 0, 0))  # loads in string in black colour
        registerTextRect = registerText.get_rect(center=(registerWidth // 2, registerHeight // 2))  # centers text
        self.registerImage.blit(registerText, registerTextRect)  # draws text onto surface
        self.registerRect = self.registerImage.get_rect()  # gets rectangle around button
        self.registerRect.topleft = (x, y)

    def loadRegisterButton(self, surface):
        surface.blit(self.registerImage, (self.registerRect.x, self.registerRect.y)) #loads button onto screen

class MenuButton(Button):
    def __init__(self, x, y, menuButtonText): #asks for coordinates and text
        super().__init__(x, y)
        self.menuButtonText = menuButtonText
        menuButtonWidth = 400
        menuButtonHeight = 80
        self.menuButtonImage = pygame.Surface((menuButtonWidth, menuButtonHeight))
        self.menuButtonImage.fill((173, 216, 230)) #light blue colour
        menuButtonFont = pygame.font.Font(None, 42)
        textToDisplay = menuButtonFont.render(self.menuButtonText, True, (0, 0, 0))
        textToDisplayRect = textToDisplay.get_rect(center=(menuButtonWidth // 2, menuButtonHeight // 2)) #centers text
        self.menuButtonImage.blit(textToDisplay, textToDisplayRect)
        self.menuButtonRect = self.menuButtonImage.get_rect()
        self.menuButtonRect.topleft = (x, y)

    def loadMenuButton(self, surface):
        surface.blit(self.menuButtonImage, (self.menuButtonRect.x, self.menuButtonRect.y))
