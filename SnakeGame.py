import pygame
import time
import random


class SnakeGame:

    def __init__(self, displayWidth, displayHeight, displayCaption, blockSize, snakeSpeed):
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.displayCaption = displayCaption
        self.blockSize = blockSize
        self.snakeSpeed = snakeSpeed

        pygame.init()
        self.display = pygame.display.set_mode((displayWidth, displayHeight))
        self.clock = pygame.time.Clock()
        self.fontStyle = pygame.font.SysFont("bahnschrift", 20)
        self.scoreFont = pygame.font.SysFont("comicsansms", 20)
        pygame.display.set_caption(displayCaption)

        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

        self.initializeSnakeVariables()

    def initializeSnakeVariables(self):
        self.snakeLength = 1
        self.snakeList = []
        self.playerScore = 0
        self.x1Change = 0
        self.y1Change = 0
        self.gameOver = False
        self.gameClose = False
        self.direction = None
        self.x1 = self.displayWidth / 2
        self.y1 = self.displayHeight / 2
        self.foodx = round(random.randrange(0, self.displayWidth - self.blockSize) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.displayHeight - self.blockSize) / 10.0) * 10.0

    def updatePlayerScore(self):
        self.playerScore = self.snakeLength - 1
        value = self.scoreFont.render("Your Score: " + str(self.playerScore), True, self.yellow)
        self.display.blit(value, [0, 0])

    def drawSnake(self):
        for x in self.snakeList:
            pygame.draw.rect(self.display, self.black, [x[0], x[1], self.blockSize, self.blockSize])

    def message(self, msg, color):
        mesg = self.fontStyle.render(msg, True, color)
        self.display.blit(mesg, [self.displayWidth / 6, self.displayHeight / 3])

    def move(self, keyEvent):
        if keyEvent == pygame.K_LEFT and self.direction != "RIGHT":
            self.x1Change = -self.blockSize
            self.y1Change = 0
            self.direction = "LEFT"
        elif keyEvent == pygame.K_RIGHT and self.direction != "LEFT":
            self.x1Change = self.blockSize
            self.y1Change = 0
            self.direction = "RIGHT"
        elif keyEvent == pygame.K_UP and self.direction != "DOWN":
            self.y1Change = -self.blockSize
            self.x1Change = 0
            self.direction = "UP"
        elif keyEvent == pygame.K_DOWN and self.direction != "UP":
            self.y1Change = self.blockSize
            self.x1Change = 0
            self.direction = "DOWN"


    def gameOverScreen(self):
        self.display.fill(self.blue)
        self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
        # self.playerScore(self.snakeLength - 1)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.gameOver = True
                    self.gameClose = False
                if event.key == pygame.K_c:
                    self.initializeSnakeVariables()
                    self.gameLoop()

    def eatFood(self):
        if self.x1 == self.foodx and self.y1 == self.foody:
            self.foodx = round(random.randrange(0, self.displayWidth - self.blockSize) / 10.0) * 10.0
            self.foody = round(random.randrange(0, self.displayHeight - self.blockSize) / 10.0) * 10.0
            self.snakeLength += 1


    # End game if snake collided with wall or itself
    def checkCollisions(self, snakeHead):
        # End game if snake collides with itself
        for x in self.snakeList[:-1]:
            if x == snakeHead:
                self.gameClose = True

        # Check if snake hit a wall
        if self.x1 >= self.displayWidth or self.x1 < 0 or self.y1 >= self.displayHeight or self.y1 < 0:
            self.gameClose = True



    def gameLoop(self):
        while not self.gameOver:

            # Game over, snake hit a wall, or itself. Show the game over screen
            while self.gameClose:
                self.gameOverScreen()

            # Move the snake, or close the game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameOver = True
                if event.type == pygame.KEYDOWN:
                    self.move(event.key)

            # Move snake
            self.x1 += self.x1Change
            self.y1 += self.y1Change
            self.display.fill(self.blue)
            pygame.draw.rect(self.display, self.green, [self.foodx, self.foody, self.blockSize, self.blockSize])
            snakeHead = [self.x1, self.y1]
            self.snakeList.append(snakeHead)
            if len(self.snakeList) > self.snakeLength:
                del self.snakeList[0]

            self.checkCollisions(snakeHead)
            self.drawSnake()
            self.eatFood()

            # Update display
            self.updatePlayerScore()
            pygame.display.update()
            self.clock.tick(self.snakeSpeed)

        pygame.quit()
        quit()


# Food collision only works with blockSize = 10 right now
width = 400
height = 400
message = "Play Snake"
blockSize = 10
speed = 15

game = SnakeGame(width, height, message, blockSize, speed)
game.gameLoop()
