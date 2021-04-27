import pygame
import time
import random
import utils
import copy

class Snake:
    def __init__(self, x, y, bounds, blockSize):
        self.x1 = x
        self.y1 = y
        self.x1Change = 0
        self.y1Change = 0
        self.snakelist = []
        self.snakelength = 1
        self.bounds = bounds
        self.blockSize = blockSize
        self.direction = None


    # End game if snake collided with wall or itself
    def checkCollisions(self, snakeHead):
        if snakeHead in self.snakelist[:-1]:
            return True

        # Check if snake hit a wall
        if snakeHead[0] >= self.bounds[0] \
                or snakeHead[0] <= 0 \
                or snakeHead[1] >= self.bounds[1] \
                or snakeHead[1] <= 0:
            return True

        return False


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


    def getChange(self, keyEvent,xChange,yChange,direction):

        if keyEvent == pygame.K_LEFT and self.direction != "RIGHT":
            xChange = -self.blockSize
            yChange = 0
            direction = "LEFT"
        elif keyEvent == pygame.K_RIGHT and self.direction != "LEFT":
            xChange = self.blockSize
            yChange = 0
            direction = "RIGHT"
        elif keyEvent == pygame.K_UP and self.direction != "DOWN":
            yChange = -self.blockSize
            xChange = 0
            direction = "UP"
        elif keyEvent == pygame.K_DOWN and self.direction != "UP":
            yChange = self.blockSize
            xChange = 0
            direction = "DOWN"
        else:
            direction = None

        return (xChange, yChange, direction)

    def getActions(self):
        return [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]


    def getValidActions(self):
        actions = []
        for action in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            (xChange, yChange, direction) = self.getChange(action, self.x1Change, self.y1Change,self.direction)
            if not direction:
                continue

            position = self.getNextPosition((self.x1, self.y1), (xChange, yChange))
            if not self.checkCollisions(position):
                actions.append((action, position))
        return actions

    def getNextPosition(self, snakehead, change):
        return (snakehead[0] + change[0], snakehead[1] + change[1])


    def getSuccessors(self):
        successors = []
        printsuccessors = []
        for action in self.getActions():
            (xChange, yChange, direction) = self.getChange(action, self.x1Change, self.y1Change, self.direction)
            if not direction:
                continue

            position = self.getNextPosition((self.x1, self.y1), (xChange, yChange))
            newSnake = copy.deepcopy(self)
            newSnake.x1 = position[0]
            newSnake.y1 = position[1]
            newSnake.x1Change = xChange
            newSnake.y1Change = yChange
            newSnake.direction = direction
            newSnake.move2(position)
            if not self.checkCollisions(position):
                successors.append((newSnake,action))
                printsuccessors.append((position,direction))
        return successors

    def move2(self,snakeHead):
        self.snakelist.append(snakeHead)
        if len(self.snakelist) > self.snakelength:
            del self.snakelist[0]


class SnakeGame:

    def __init__(self, displayWidth, displayHeight, displayCaption, blockSize, snakeSpeed, agent = None):
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.blockSize = blockSize
        self.bounds = (self.displayWidth - self.blockSize, self.displayHeight - self.blockSize)
        self.snakeSpeed = snakeSpeed
        self.agent = agent

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
        self.playerScore = 0
        self.gameOver = False
        self.gameClose = False
        self.snake = Snake(self.displayWidth / 2, self.displayHeight / 2, self.bounds, self.blockSize)
        self.spawnFood()

    def spawnFood(self):
        while True:
            self.foodx = round(random.randrange(self.blockSize, self.displayWidth - (self.blockSize * 2)) / self.blockSize) * self.blockSize
            self.foody = round(random.randrange(self.blockSize, self.displayHeight - (self.blockSize * 2)) / self.blockSize) * self.blockSize
            if (self.foodx,self.foody) not in self.snake.snakelist:
                break

    def updatePlayerScore(self):
        self.playerScore = self.snake.snakelength - 1
        value = self.scoreFont.render("Your Score: " + str(self.playerScore), True, self.yellow)
        self.display.blit(value, [0, 0])

    def drawSnake(self):
        for x in self.snake.snakelist:
            pygame.draw.rect(self.display, self.black, [x[0], x[1], self.blockSize, self.blockSize])

    def message(self, msg, color):
        mesg = self.fontStyle.render(msg, True, color)
        self.display.blit(mesg, [self.displayWidth / 6, self.displayHeight / 3])




    def gameOverScreen(self):
        self.display.fill(self.blue)
        self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
        # self.playerScore(self.snake.snakelength - 1)
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
        if self.snake.x1 == self.foodx and self.snake.y1 == self.foody:
            self.spawnFood()
            self.snake.snakelength += 1





    def gameLoop(self):
        while not self.gameOver:

            # Game over, snake hit a wall, or itself. Show the game over screen
            while self.gameClose:
                self.gameOverScreen()

            if self.agent:
                nextMove = self.agent.selectMove(self.snake, (self.foodx, self.foody))
                if nextMove:
                    newEvent = pygame.event.Event(pygame.KEYDOWN, unicode="a", key=nextMove,
                                                  mod=pygame.KMOD_NONE)
                    pygame.event.post(newEvent)

            # Move the snake, or close the game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameOver = True
                if event.type == pygame.KEYDOWN:
                    self.snake.move(event.key)

            # Move snake
            self.snake.x1 += self.snake.x1Change
            self.snake.y1 += self.snake.y1Change
            self.display.fill(self.blue)
            pygame.draw.rect(self.display, self.green, [self.foodx, self.foody, self.blockSize, self.blockSize])
            snakeHead = [self.snake.x1, self.snake.y1]
            self.snake.move2(snakeHead)

            if self.snake.checkCollisions(snakeHead):
                self.gameClose = True

            self.drawSnake()
            self.eatFood()

            # Update display
            self.updatePlayerScore()
            pygame.display.update()
            self.clock.tick(self.snakeSpeed)

        pygame.quit()
        quit()




class ManhattanAgent:

    def selectMove(self, snake, food):
        bestDistance = float("inf")
        bestAction = None

        for action, position in snake.getValidActions():
            distance = manhattanHeuristic(position, food)
            if distance < bestDistance:
                bestDistance = distance
                bestAction = action

        return bestAction


class AStarAgent:

    def __init__(self):
        self.path = []
        self.goal = None

    def selectMove(self, snake, food):
        if not self.goal or self.goal != food:
            self.path = self.computePath(snake, food)
        if not self.path:
            self.path = self.computePath(snake,food)

        if not self.path:
            return None

        nextMove = self.path.pop(0)
        return nextMove

    def computePath(self, snake, food):
        frontier = utils.myPriorityQueue(food, self.aStarHelperFn)
        state = (snake,[])
        explored = set()
        frontier.push(state, manhattanHeuristic)

        while not frontier.isEmpty():
            node = frontier.pop()
            position = (node[0].x1, node[0].y1)
            if (node[0].x1, node[0].y1) == food:
                return node[1]
            if position in explored:
                continue
            explored.add(position)
            for child in node[0].getSuccessors():
                childposition = (child[0].x1,child[0].y1)
                if childposition not in explored:
                    frontier.push((child[0], node[1]+[child[1]]), manhattanHeuristic)
        return []

    #state = (snake,list of actions so far)
    def aStarHelperFn(self, state, goal, heuristic):
        # print((heuristic((state[0].x1, state[0].y1), goal) // state[0].blockSize))
        return len(state[1]) + (heuristic((state[0].x1, state[0].y1), goal) // state[0].blockSize)


# Referenced from pacman project
def manhattanHeuristic(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])






width = 600
height = 600
message = "Play Snake"
blockSize = 20
speed = 20

agent = ManhattanAgent()
aStarAgent = AStarAgent()

# game = SnakeGame(width, height, message, blockSize, speed, agent)
game = SnakeGame(width, height, message, blockSize, speed, aStarAgent)

game.gameLoop()
