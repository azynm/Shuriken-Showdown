import pygame
from pygame import *
#import bcrypt
import sqlite3
import sys
import random
from random import *
from random import randint
from random import choice
#the above imports the essential modules required
# * means import all
pygame.init()
clock = pygame.time.Clock()
fps = 60 #sets the frame rate for the screens
import buttons
import characters
import projectile
class screen():
    def __init__(self, color, username): #constructor
        self.color = color
        self.username = username # name of player who is signed in
        self.outputScreen = pygame.display.set_mode((2048, 1152), FULLSCREEN) #loads screen
        pygame.display.set_caption('SHURIKEN SHOWDOWN')  # decides name of window
        self.outputScreen.fill(self.color)

        self.ScreenWidth = self.outputScreen.get_width()
        self.ScreenHeight = self.outputScreen.get_height()

    # note to self: home monitor resolution is Width: 2048 Height: 1152 (2048, 1152), FULLSCREEN



    def handler(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit() #exits game
                    sys.exit()
            clock.tick(fps)
            pygame.display.flip() #refreshes screen


class RegistrationScreen(screen): #inherits attributes and methods from superclass
    def __init__(self, color, username):
        super().__init__(color, username)
        #loads sign-in button
        self.signInButton = buttons.SignInButton(self.ScreenWidth * 0.005, self.ScreenHeight * 0.75)
        self.signInButton.loadSigninButton(self.outputScreen)
        #loads register button
        self.RegisterButton = buttons.RegistrationButton(self.ScreenWidth * 0.85, self.ScreenHeight * 0.75)
        self.RegisterButton.loadRegisterButton(self.outputScreen)

        self.width = self.outputScreen.get_width()
        self.height = self.outputScreen.get_height()


        #code for title
        self.TitleFont = pygame.font.Font(None, 82)
        self.TitleText = 'SHURIKEN SHOWDOWN'
        self.TitleSurface = self.TitleFont.render(self.TitleText, True, (255, 255, 255))
        titleWidth, titleHeight = self.TitleFont.size(self.TitleText)
        titlex = (self.width - titleWidth) // 2  #finds x-coordinate to use in centering
        titley = 100
        self.outputScreen.blit(self.TitleSurface, (titlex, titley))



        # set-up code for text creation
        self.boxFont = pygame.font.Font(None, 42) #none sets font to default

        #username box
        self.userBoxText = '' #blank text
        self.userBoxsurface = self.boxFont.render(self.userBoxText, True, (0, 0, 0)) #draws black text
        self.outputScreen.blit(self.userBoxsurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35))
        #outputs text to screen

        self.UserBoxArea = ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35, 400, 80) #creates surface for box
        self.outputScreen.fill((255, 255, 255), self.UserBoxArea) #makes box white
        self.UserBoxActive = False #default state is dormant

        #password box
        self.PassBoxText = ''
        self.PassBoxSurface = self.boxFont.render(self.userBoxText, True, (0, 0, 0))
        self.outputScreen.blit(self.PassBoxSurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.5))

        self.PassBoxArea = ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.5, 400, 80)
        self.outputScreen.fill((255, 255, 255), self.PassBoxArea)
        self.PassBoxActive = False

    # username validation
    def username_check(self, submitted_username):
        # username must be at least 5 characters long and alphanumeric
        if len(submitted_username) < 5:
            print('username too short')
            return False
        if submitted_username.isalnum() == False:
            print('alphanumeric only')
            return False
        else:
            print('valid username')
            return True

    def password_check(self, submitted_password):
        # password must be at least 8 characters long
        if len(submitted_password) < 8:
            print('password too short')
            return False
        else:
            print('Valid password')
            return True


    def create_database(self):
        link = sqlite3.connect('players.db')  # creates a connection to the database so it can be interacted with
        cursor = link.cursor()  # creates a cursor to interact with the database through

        # creates the players table if it can't be found in the database
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
        PlayerID INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        high_score INTEGER DEFAULT 0
        )
        ''')
        link.close()

    def register_account(self, username, password):
        link = sqlite3.connect('players.db')
        cursor = link.cursor()

        try: # attempts to run the indented code
            cursor.execute('''
            INSERT INTO players (username, password) VALUES (?, ?)
            ''', (username, password))
            link.commit()  # saves change made to database
        except sqlite3.IntegrityError: # does not carry out change if username is not unique
            print('Username taken')
        finally:
            link.close() # closes connection allowing for other queries to be made

    def sign_in(self, username, password):
        link = sqlite3.connect('players.db')
        cursor = link.cursor()

        # query to find appropriate password
        cursor.execute('''
        SELECT password FROM players WHERE username=?''', (username,))
        fetchedPassword = cursor.fetchone() # returns tuple of attributes queried, or none if non-existent
        link.close()

        # only branches if a password could be found
        if fetchedPassword:
            if fetchedPassword[0] == password:  # checks for  a match
                print('signed in')
                return True
            else:
                print('incorrect password')
                return False
        else:  # runs if no username found in database
            print('account not found')
            return False






    def register_handler(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # exits game
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #specifies that left click is wanted
                        mousex, mousey = pygame.mouse.get_pos() #returns mouse coordinates



                        if self.signInButton.signInRect.collidepoint(mousex, mousey): #collision detection
                            submitted_username = self.userBoxText
                            submitted_password = self.PassBoxText
                            if self.sign_in(submitted_username, submitted_password): # only carries on when signed-in
                                username = submitted_username
                                self.outputScreen.fill((0, 0, 139)) # goes to main menu
                                main_menu = MainMenu((0, 0, 139), username)
                                main_menu.mainMenuHandler()

                        elif self.RegisterButton.registerRect.collidepoint(mousex, mousey): #collision detection
                            # takes whatever is currently in the text boxes
                            submitted_username = self.userBoxText
                            submitted_password = self.PassBoxText


                            # runs validation checks on credentials
                            if self.username_check(submitted_username) and self.password_check(submitted_password):
                                self.register_account(submitted_username, submitted_password)


                        if pygame.Rect(*self.UserBoxArea).collidepoint(mousex, mousey):
                            self.UserBoxActive = True #activates username box, deactivates password box
                            self.PassBoxActive = False
                        elif pygame.Rect(*self.PassBoxArea).collidepoint(mousex, mousey):
                            self.PassBoxActive = True #activates password box, deactivates username box
                            self.UserBoxActive = False
                        else:
                            self.UserBoxActive = False #deactivates both
                            self.PassBoxActive = False
                            #outline management
                    if self.UserBoxActive:
                        user_outline = (self.UserBoxArea[0] - 2, self.UserBoxArea[1] - 2, self.UserBoxArea[2] + 4,
                                        self.UserBoxArea[3] + 4) #creates hollow rect around text box
                        pygame.draw.rect(self.outputScreen, (255, 255, 0), user_outline, 2) #yellow outline
                    else:
                        user_outline = (self.UserBoxArea[0] - 2, self.UserBoxArea[1] - 2, self.UserBoxArea[2] + 4,
                                        self.UserBoxArea[3] + 4)
                        pygame.draw.rect(self.outputScreen, self.color, user_outline, 2) #transparent outline

                    if self.PassBoxActive:
                        pass_outline = (self.PassBoxArea[0] - 2, self.PassBoxArea[1] - 2, self.PassBoxArea[2] + 4,
                                        self.PassBoxArea[3] + 4)
                        pygame.draw.rect(self.outputScreen, (255, 255, 0), pass_outline, 2)
                    else:
                        pass_outline = (self.PassBoxArea[0] - 2, self.PassBoxArea[1] - 2, self.PassBoxArea[2] + 4,
                                        self.PassBoxArea[3] + 4)
                        pygame.draw.rect(self.outputScreen, self.color, pass_outline, 2)

                elif event.type == pygame.KEYDOWN and self.UserBoxActive == True:
                    if event.key == pygame.K_BACKSPACE:
                        self.userBoxText = self.userBoxText[:-1]
                        self.userBoxsurface = self.boxFont.render(self.userBoxText, True, (0, 0, 0))
                        self.outputScreen.blit(self.userBoxsurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35))


                    elif len(self.userBoxText) < 10:
                        self.userBoxText += event.unicode #adds key pressed to string
                        self.userBoxsurface = self.boxFont.render(self.userBoxText, True, (0, 0, 0))
                        #above redraws the textbox with the updated text
                        self.outputScreen.blit(self.userBoxsurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35))

                    self.outputScreen.fill((255, 255, 255), self.UserBoxArea) #clear the text box

                    self.userBoxsurface = self.boxFont.render(self.userBoxText, True, (0, 0, 0)) #write the new text
                    self.outputScreen.blit(self.userBoxsurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35))

                elif event.type == pygame.KEYDOWN and self.PassBoxActive == True:
                    if event.key == pygame.K_BACKSPACE:
                        self.PassBoxText = self.PassBoxText[:-1]
                        self.PassBoxSurface = self.boxFont.render(self.PassBoxText, True, (0, 0, 0))
                        self.outputScreen.blit(self.PassBoxSurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.5))


                    elif len(self.PassBoxText) < 15:
                        self.PassBoxText += event.unicode #adds key pressed to string
                        self.PassBoxSurface = self.boxFont.render(self.PassBoxText, True, (0, 0, 0))
                        #above redraws the textbox with the updated text
                        self.outputScreen.blit(self.PassBoxSurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.5))

                    self.outputScreen.fill((255, 255, 255), self.PassBoxArea) #clear the text box

                    self.PassBoxSurface = self.boxFont.render(self.PassBoxText, True, (0, 0, 0)) #write the new text
                    self.outputScreen.blit(self.PassBoxSurface, ((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.5))

                elif event.type == pygame.KEYDOWN and self.PassBoxActive == False and self.UserBoxActive == False:
                    if event.key == pygame.K_q:
                        pygame.quit()  # exits game
                        sys.exit()

            clock.tick(fps)
            pygame.display.flip()  # refreshes screen


class MainMenu(screen):
    def __init__(self, color, username): #constructor methods
        super().__init__(color, username)

        self.startButton = buttons.MenuButton((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35, 'START')
        self.startButton.loadMenuButton(self.outputScreen)
        self.leaderboardButton = buttons.MenuButton((self.ScreenWidth - 400) / 2,self.ScreenHeight * 0.45, 'LEADERBOARD')
        self.leaderboardButton.loadMenuButton(self.outputScreen)
        self.controlButton = buttons.MenuButton((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.55, 'CONTROLS')
        self.controlButton.loadMenuButton(self.outputScreen)
        self.quitButton = buttons.MenuButton((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.65, 'EXIT')
        self.quitButton.loadMenuButton(self.outputScreen)

    def mainMenuHandler(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # exits game
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousex, mousey = pygame.mouse.get_pos()
                        if self.startButton.menuButtonRect.collidepoint(mousex, mousey):
                            gameloop = GameMap((0, 0, 0), self.username)
                            gameloop.GameMapHandler()
                        elif self.leaderboardButton.menuButtonRect.collidepoint(mousex, mousey):
                            leaderboard = Leaderboard((0, 0, 139), self.username)
                            leaderboard.LeaderboardHandler()
                        elif self.quitButton.menuButtonRect.collidepoint(mousex, mousey):
                            pygame.quit()  # exits game
                            sys.exit()
                        elif self.controlButton.menuButtonRect.collidepoint(mousex, mousey):
                            controlscreen = ControlScreen((0, 0, 139), self.username)
                            controlscreen.ControlScreenHandler()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()  # exits game
                        sys.exit()


                clock.tick(fps)
                pygame.display.flip()  # refreshes screen

class Leaderboard(screen):
    def __init__(self, color, username):
        super().__init__(color, username)

        # text at the top of the screen
        self.LeaderboardFont = pygame.font.Font(None, 82)  # font for below text
        self.LeaderboardText = 'High Scores'  # text to display
        self.TitleSurface = self.LeaderboardFont.render(self.LeaderboardText, True, (255, 255, 255))
        textWidth, textHeight = self.LeaderboardFont.size(self.LeaderboardText)
        font_x = (self.ScreenWidth - textWidth) // 2  # finds x-coordinate to use in centering
        font_y = 50
        self.outputScreen.blit(self.TitleSurface, (font_x, font_y))  # outputs to screen

        # button to go back to main menu
        self.backButton = buttons.MenuButton(20, 20, 'BACK')
        self.backButton.loadMenuButton(self.outputScreen)

        link = sqlite3.connect('players.db')
        cursor = link.cursor()
        # get up to 10 highest scorers from database
        cursor.execute('SELECT username, high_score FROM players ORDER BY high_score DESC LIMIT 10')
        self.fetchedScores = cursor.fetchall()
        link.close()

        # vertical starting point for text
        initialY = 200

        self.scoresFont = pygame.font.Font(None, 64)
        # print each element of the string

        # does this for all items in fetchedScores
        for score, (username, high_score) in enumerate(self.fetchedScores, start=1):
            # includes rank, name and score
            scoreLine = f"{score}. {username}- {high_score}" # concatenates variables inside the string
            scoresSurface = self.scoresFont.render(scoreLine, True, (255, 255, 255)) # surface for score to be output
            scoresRect = scoresSurface.get_rect(center=(self.ScreenWidth / 4, initialY + (score - 1) * 50))
            # ^ calculations to centre the scores
            self.outputScreen.blit(scoresSurface, scoresRect) # displays scores on screen

        # Update the display
        pygame.display.flip()

    def LeaderboardHandler(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # exits game
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()  # exits game
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousex, mousey = pygame.mouse.get_pos()
                        print(mousex, mousey)
                        if self.backButton.menuButtonRect.collidepoint(mousex, mousey):
                            self.outputScreen.fill((0, 0, 139))
                            main_menu = MainMenu((0, 0, 139), self.username)
                            main_menu.mainMenuHandler()

class ControlScreen(screen):
    def __init__(self, color, username):
        super().__init__(color, username)

        self.controlScreenWidth = self.outputScreen.get_width()
        self.controlScreenHeight = self.outputScreen.get_height()


        self.backButton = buttons.MenuButton(20, 20, 'BACK')
        self.backButton.loadMenuButton(self.outputScreen)
        self.TitleFont = pygame.font.Font(None, 46)
        self.ControlText = [
            "Movement: WASD",
            "Shoot: Arrow Keys",
            "Pause: P",
            "Instructions:",
            "Avoid being hit and eliminate enemies to earn points!"
        ] # above is a list of strings that will be run through and printed

        # Calculate the starting y position to center the instructions vertically
        startingTextHeight = len(self.ControlText) * 46
        initialY = (self.controlScreenHeight - startingTextHeight) / 2

        # print each element of the string
        for i, line in enumerate(self.ControlText): #gets vertical index for use in positioning
            controlTextsurface = self.TitleFont.render(line, True, (255, 255, 255)) #renders text onto surface
            controlTextRect = controlTextsurface.get_rect(center=(self.controlScreenWidth / 2, initialY + i * 46)) #centers text
            self.outputScreen.blit(controlTextsurface, controlTextRect) #displays text on screen

        # Update the display
        pygame.display.flip()

    def ControlScreenHandler(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # exits game
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousex, mousey = pygame.mouse.get_pos()
                        if self.backButton.menuButtonRect.collidepoint(mousex, mousey):
                            self.outputScreen.fill((0, 0, 139))
                            main_menu = MainMenu((0, 0, 139), self.username)
                            main_menu.mainMenuHandler()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()  # exits game
                        sys.exit()

class gameOverScreen(screen):
    def __init__(self, color, finalScore, username): # constructor
        super().__init__(color, username)

        # obtains screen parameters
        self.gameOverWidth = self.outputScreen.get_width()
        self.gameOverHeight = self.outputScreen.get_height()
        self.finalScore = str(finalScore) # variable that passes in the player's score upon death

        self.infoFont = pygame.font.Font(None, 80)

        # initialise and load buttons
        self.tryAgainButton = buttons.MenuButton((self.gameOverWidth - 400) / 2, self.gameOverHeight * 0.45, 'TRY AGAIN')
        self.tryAgainButton.loadMenuButton(self.outputScreen)

        self.toMenuButton = buttons.MenuButton((self.gameOverWidth - 400) / 2, self.gameOverHeight * 0.55, 'TO MENU')
        self.toMenuButton.loadMenuButton(self.outputScreen)

        # text to be displayed
        self.information = [
            'GAME OVER',
            ' ',
            'Final Score was ' + self.finalScore
        ]

        # Calculate the starting y position to center the instructions vertically
        startingTextHeight = len(self.information) * 46
        initialY = (self.gameOverHeight - startingTextHeight) / 6

        # print each element of the string
        for i, line in enumerate(self.information):  # gets vertical index for use in positioning
            infoTextSurface = self.infoFont.render(line, True, (255, 255, 255))  # renders text onto surface
            infoTextRect = infoTextSurface.get_rect(
                center=(self.gameOverWidth / 2, initialY + i * 46))  # centers text
            self.outputScreen.blit(infoTextSurface, infoTextRect)  # displays text on screen

        # Update the display
        pygame.display.flip()

    def gameOverScreenHandler(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # exits game
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()  # exits game
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousex, mousey = pygame.mouse.get_pos()
                        print(mousex, mousey)
                        if self.toMenuButton.menuButtonRect.collidepoint(mousex, mousey):
                            self.outputScreen.fill((0, 0, 139)) # resets screen
                            main_menu = MainMenu((0, 0, 139), self.username)  # goes back to main menu
                            print('main menu accessed')
                            main_menu.mainMenuHandler()
                        if self.tryAgainButton.menuButtonRect.collidepoint(mousex, mousey):
                            self.outputScreen.fill((0, 0, 139))  # resets screen
                            gameloop = GameMap((0, 0, 0), self.username)
                            print('game restarted')
                            gameloop.GameMapHandler() # starts game again




class GameMap(screen):
    def __init__(self, color, username):
        super().__init__(color, username)
        self.pixelWidth = 2048 # parameters for dimensions
        self.pixelHeight = 1152
        self.tileSize = 64
        self.mapWidth = 32
        self.mapHeight = 18

        self.playerPositionx = 16 * self.tileSize
        self.playerPositiony = 9 * self.tileSize

        self.ThePlayer = characters.player(500, self.playerPositionx, self.playerPositiony, 20)
        self.playerHealthBar = characters.healthBar(20, 20, 200, 50, self.ThePlayer.health)

        self.activeShuriken = pygame.sprite.Group() # group for all shurikens
        self.initialShotTime = 0
        self.shurikenCooldown = 1000 # 1 second cooldown between throws

        self.cyclopsGroup = pygame.sprite.Group()
        self.initialHitTime = 0
        self.playerHitCooldown = 2000 # player can only be hit every 2 seconds

        self.timeSinceCyclopsSpawn = 0 # last time a cyclops spawned in
        self.cyclopsCooldown = 1 # 3 second cooldown

        self.timeSinceDragonSpawn = 0 # last time a dragon spawned in
        self.dragonCooldown = 1 # 1 second cooldown

        self.dragonGroup = pygame.sprite.Group()

        self.fireballGroup = pygame.sprite.Group()
        self.initialFireTime = 0 # time since last shot
        self.fireballCooldown = 2000 # 2 second cooldown between shots

        self.playerScore = 0 # initialises player score
        self.scoreFont = pygame.font.Font(None, 42) # word data for displaying score

        # initial spawn limits for enemies
        self.cyclopsLimit = 1
        self.dragonLimit = -1
        self.lastCheckpoint = 0

        self.paused = False




        self.fieldTile = pygame.transform.scale(pygame.image.load('assets/GrassTile.png'), (self.tileSize, self.tileSize))
        self.enemyTile = pygame.transform.scale(pygame.image.load('assets/enemyTile.png'), (self.tileSize, self.tileSize))
        # loads in field tile and upscales it to match the tile size
        # 2D list containing tiles
        self.map = [
            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e','e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j','j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'],
            ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e','e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']

              ]
    # for each item in the list, loads the appropriate image
    def loadMap(self):
        rowCount = 0 # start at first row
        for row in self.map:
            columnCount = 0 # start at first item
            for tile in row: # goes through each item in a row
                if tile == 'j':
                    position_x = columnCount * self.tileSize # finds the right coordinates to place tile at
                    position_y = rowCount * self.tileSize
                    self.outputScreen.blit(self.fieldTile, (position_x, position_y))
                if tile == 'e':
                    position_x = columnCount * self.tileSize
                    position_y = rowCount * self.tileSize
                    self.outputScreen.blit(self.enemyTile, (position_x, position_y))

                columnCount += 1  # move to the next column
            rowCount += 1  # move to the next row

    #  compares score on death to score held in database
    def checkForHighScore(self, username, finalScore):
        link = sqlite3.connect('players.db')
        cursor = link. cursor()
        # find current high score in database using the username
        cursor.execute('SELECT high_score FROM players WHERE username =?', (username,))
        result = cursor.fetchone() # returns high score as an element in a tuple
        if result is None: #  if database hasn't updated correctly and user isnt found
            print('user cannot be found')
        else:
            current_high_score = result[0]
            # score comparisons
            if int(finalScore) > current_high_score:
                # update score
                cursor.execute('UPDATE players SET high_score=? WHERE username=?', (finalScore, username))
                link.commit()
        link.close()


    def showScore(self):
        playerScoreSurface = self.scoreFont.render('Score: ' + str(self.playerScore), True, (255, 255, 255)) # concatenates score onto string
        playerScoreRect = playerScoreSurface.get_rect(topright=(self.pixelWidth - 150, 20)) # positions the top right of the rect 20x20 pixels away from the corner
        self.outputScreen.blit(playerScoreSurface, playerScoreRect) # outputs score to screen


    def GameMapHandler(self):
        running = True
        while running:
            timeNow = pygame.time.get_ticks()
            self.loadMap()  # redraw the map
            self.ThePlayer.movePlayer()  # update player position based on input
            self.playerHealthBar.loadBar(self.outputScreen) # draw health bar
            self.outputScreen.blit(self.ThePlayer.image, self.ThePlayer.rect)  # draw the player
            self.activeShuriken.update() # updates sprite group
            self.activeShuriken.draw(self.outputScreen) # redraws shuriken in new positions
            self.showScore() # outputs current score
            self.dragonGroup.draw(self.outputScreen)  # update positions of all dragons
            self.fireballGroup.update()  # updates sprite group
            self.fireballGroup.draw(self.outputScreen)  # redraws fireballs in new position

            if self.playerScore - self.lastCheckpoint >= 500:
                self.cyclopsLimit += 1
                self.dragonLimit += 1
                self.lastCheckpoint = self.playerScore

            for cyclops in self.cyclopsGroup:
                cyclops.update(self.ThePlayer.rect.x, self.ThePlayer.rect.y)
            self.cyclopsGroup.draw(self.outputScreen)

            # (group 1, group 2, de-spawn group 1, de-spawn group 2)
            cyclopsHitCheck = pygame.sprite.groupcollide(self.cyclopsGroup, self.activeShuriken, False, True)
            for cyclops in cyclopsHitCheck: # checks every instance of a cyclops
                for shuriken in cyclopsHitCheck[cyclops]: # for every time a cyclops is hit, decrease health
                    cyclops.remainingHealth -= 50
                    if cyclops.remainingHealth <=0:
                        self.playerScore += cyclops.cyclopsValue # adds to score if enemy dies



            dragonHitCheck = pygame.sprite.groupcollide(self.dragonGroup, self.activeShuriken, False, True)
            for dragon in dragonHitCheck: # checks every alive dragon
                for shuriken in dragonHitCheck[dragon]: # for every instance of a collision
                    dragon.remainingHealth -= 50 # damage dragon
                    if dragon.remainingHealth <=0: # death check
                        self.playerScore += dragon.dragonValue # if enemy dies, increase score

            # 'True' despawns fireball on hit
            fireballHitPlayerCheck = pygame.sprite.spritecollide(self.ThePlayer, self.fireballGroup, True)
            for fireball in fireballHitPlayerCheck:
                if timeNow - self.initialHitTime > self.playerHitCooldown: # only registers after cooldown
                    self.ThePlayer.remainingHealth -= 40 # decreases health
                    self.playerHealthBar.hp = self.ThePlayer.remainingHealth # healthbar matches player
                    self.initialHitTime = timeNow # updates time since hit




            # (sprite, group, de-spawn group)
            cyclopsHitPlayerCheck = pygame.sprite.spritecollide(self.ThePlayer, self.cyclopsGroup, False)
            for cyclops in cyclopsHitPlayerCheck: # for each cyclops that hits the player, decrease health
                if timeNow - self.initialHitTime > self.playerHitCooldown: # only registers hit after cooldown
                    self.ThePlayer.remainingHealth -= 40
                    self.playerHealthBar.hp = self.ThePlayer.remainingHealth # health bar matches player
                    self.initialHitTime = timeNow # updates time since last shot

            # (sprite, group, de-spawn group)
            dragonHitPlayerCheck = pygame.sprite.spritecollide(self.ThePlayer, self.dragonGroup, False)
            for dragon in dragonHitPlayerCheck: # for each dragon that hits the player, decrease health
                if timeNow - self.initialHitTime > self.playerHitCooldown: # only registers hit after cooldown
                    self.ThePlayer.remainingHealth -= 40
                    self.playerHealthBar.hp = self.ThePlayer.remainingHealth # health bar matches player
                    self.initialHitTime = timeNow # updates time since last shot




            for dragon in self.dragonGroup: # happens for every active dragon
                dragon.update(self.ThePlayer.rect.x, self.ThePlayer.rect.y) # player coords as parameters
                if abs(dragon.rect.x - self.ThePlayer.rect.x) < 15 and timeNow - self.initialFireTime > self.fireballCooldown:
                    #^ for vertical fireball if less than 15 pixels apart, if cooldown has been passed
                    self.initialFireTime = timeNow
                    if dragon.rect.y > self.ThePlayer.rect.y:
                        fireball = projectile.yfireball(dragon.rect.x, dragon.rect.y, -20, 50) # will move up
                        self.fireballGroup.add(fireball) # add to sprite group
                        fireball.update() # movement function
                    elif dragon.rect.y < self.ThePlayer.rect.y:
                        fireball = projectile.yfireball(dragon.rect.x, dragon.rect.y, 20, 50) # will move down
                        self.fireballGroup.add(fireball)
                        fireball.update()

                if abs(dragon.rect.y - self.ThePlayer.rect.y) < 15 and timeNow - self.initialFireTime > self.fireballCooldown:
                    #^ for horizontal fireball if less than 15 pixels apart
                    self.initialFireTime = timeNow
                    if dragon.rect.x > self.ThePlayer.rect.x:
                        fireball = projectile.xfireball(dragon.rect.x, dragon.rect.y, -20, 50) # will go left
                        self.fireballGroup.add(fireball)
                        fireball.update()
                    elif dragon.rect.x < self.ThePlayer.rect.x:
                        fireball = projectile.xfireball(dragon.rect.x, dragon.rect.y, 20, 50) # will go right
                        self.fireballGroup.add(fireball)
                        fireball.update()


            # spawns only if there are less than 8 total enemies and the cooldown has been reached
            if len(self.cyclopsGroup) < self.cyclopsLimit and (timeNow - self.timeSinceCyclopsSpawn > self.cyclopsCooldown):
                spawnTiles = [] # creates list of spawn tiles
                rowCount = 0
                for row in self.map: # iterates for every row
                    columnCount = 0
                    for tile in row: # iterates for every item within a row
                        if tile == 'e':
                            position_x = columnCount * self.tileSize
                            position_y = rowCount * self.tileSize

                            spawnTiles.append((position_x, position_y)) # gets all spawn tile coordinates
                        columnCount += 1
                    rowCount += 1

                if spawnTiles and randint(1, 10) == 1: # 1 in 2000 chance to spawn
                        position_x, position_y = choice(spawnTiles)
                        newCyclops = characters.cyclops(100, position_x, position_y, 5, 100)  # instantiates enemy
                        self.cyclopsGroup.add(newCyclops)  # adds to sprite group
                        self.timeSinceCyclopsSpawn = timeNow # updates time since last spawn


            if self.playerScore > 1000:
                # spawns only if there are less than 8 total enemies and the cooldown has been reached
                if len(self.dragonGroup) < self.dragonLimit and (timeNow - self.timeSinceCyclopsSpawn > self.cyclopsCooldown):
                    spawnTiles = [] # creates list of spawn tiles
                    rowCount = 0
                    for row in self.map:
                        columnCount = 0
                        for tile in row:  # iterates for every item within a row
                            if tile == 'e':
                                position_x = columnCount * self.tileSize
                                position_y = rowCount * self.tileSize

                                spawnTiles.append((position_x, position_y))  # gets all spawn tile coordinates
                            columnCount += 1
                        rowCount += 1

                    if spawnTiles and randint(1, 20) == 1: # 1 in 3000 chance to spawn:
                        position_x, position_y = choice(spawnTiles)
                        newDragon = characters.dragon(300, position_x, position_y, 4, 200) # instantiates enemy
                        self.dragonGroup.add(newDragon) # adds to sprite group
                        self.timeSinceDragonSpawn = timeNow # updates time since last spawn




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # exits game
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()  # exits game
                        sys.exit()


                    if event.key == pygame.K_p: # detects for a press of P
                        self.paused = True # pause screen runs while this condition is true


                    # shooting code
                    if event.key == pygame.K_UP and timeNow - self.initialShotTime > self.shurikenCooldown:
                        self.initialShotTime = timeNow # resets shot cooldown timer
                        # creates shuriken that will travel in the appropriate direction
                        star = projectile.yshuriken(self.ThePlayer.rect.x, self.ThePlayer.rect.y, -30, 50)
                        self.activeShuriken.add(star) # adds to sprite group
                        star.update()
                    if event.key == pygame.K_DOWN and timeNow - self.initialShotTime > self.shurikenCooldown:
                        self.initialShotTime = timeNow
                        star = projectile.yshuriken(self.ThePlayer.rect.x, self.ThePlayer.rect.y, 30, 50)
                        self.activeShuriken.add(star)
                        star.update()
                    if event.key == pygame.K_LEFT and timeNow - self.initialShotTime > self.shurikenCooldown:
                        self.initialShotTime = timeNow
                        star = projectile.xshuriken(self.ThePlayer.rect.x, self.ThePlayer.rect.y, -30, 50)
                        self.activeShuriken.add(star)
                        star.update()
                    if event.key == pygame.K_RIGHT and timeNow - self.initialShotTime > self.shurikenCooldown:
                        self.initialShotTime = timeNow
                        star = projectile.xshuriken(self.ThePlayer.rect.x, self.ThePlayer.rect.y, 30, 50)
                        self.activeShuriken.add(star)
                        star.update()




            if self.paused == True:
                while self.paused == True:
                    # pauseOverlay = pygame.Surface((self.ScreenWidth, self.ScreenHeight), pygame.SRCALPHA)
                    # pauseOverlay.fill((0, 0, 0, 100))  # black
                    # self.outputScreen.blit(pauseOverlay, (0, 0))  # draws overlay
                    # instantiates buttons
                    continueButton = buttons.MenuButton((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.35,
                                                        'CONTINUE')
                    quitButton = buttons.MenuButton((self.ScreenWidth - 400) / 2, self.ScreenHeight * 0.45,
                                                    'QUIT')
                    # loads buttons onto screen
                    continueButton.loadMenuButton(self.outputScreen)
                    quitButton.loadMenuButton(self.outputScreen)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                pygame.quit()  # exits game
                                sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # left click
                                mousex, mousey = pygame.mouse.get_pos()  # gets coordinates of click
                                print(mousex, mousey)
                                if continueButton.menuButtonRect.collidepoint(mousex, mousey):
                                    self.paused = False  # condition to end loop
                                if quitButton.menuButtonRect.collidepoint(mousex, mousey):
                                    self.outputScreen.fill((0, 0, 139))  # resets screen
                                    main_menu = MainMenu((0, 0, 139), self.username)  # goes back to main menu
                                    main_menu.mainMenuHandler()

                    pygame.display.flip()  # update display

            if self.ThePlayer.remainingHealth <= 0: #checks for player death
                finalScore = self.playerScore # creates variable for player's score upon death
                self.checkForHighScore(self.username, finalScore)  # check for new high score
                self.outputScreen.fill((0, 0, 139)) # reset screen
                game_over_screen = gameOverScreen((0, 0, 139), finalScore, self.username) # goes to game over screen
                game_over_screen.gameOverScreenHandler()


            pygame.display.flip()  # refreshes screen
            clock.tick(fps)
