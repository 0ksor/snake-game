import pygame
import random

CELL_SIZE = 10
GREEN = (0, 255, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)


class SnakeGame:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h

        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset_game()
        self.speed = 10
        self.move_interval = 1000 // self.speed
        self.last_move_time = 0
        self.paused = False

    def random_food(self):
        return (random.randrange(0, self.width, CELL_SIZE),
                random.randrange(0, self.height, CELL_SIZE))

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_k] and self.direction != (0, CELL_SIZE):
            self.direction = (0, -CELL_SIZE)
        if keys[pygame.K_j] and self.direction != (0, -CELL_SIZE):
            self.direction = (0, CELL_SIZE)
        if keys[pygame.K_h] and self.direction != (CELL_SIZE, 0):
            self.direction = (-CELL_SIZE, 0)
        if keys[pygame.K_l] and self.direction != (-CELL_SIZE, 0):
            self.direction = (CELL_SIZE, 0)

    def move(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.random_food()
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        return (
            head in self.snake[1:] or
            head[0] < 0 or head[1] < 0 or
            head[0] >= self.width or head[1] >= self.height
        )

    def draw(self):
        self.screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN,
                             (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED, (*self.food, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont(None, 36)
        speed_text = font.render(f"Speed: {self.speed}", True, (255, 255, 255))
        self.screen.blit(speed_text, (5, 5))

        pygame.display.flip()

    def reset_game(self):
        self.snake = [(100, 100)]
        self.direction = (CELL_SIZE, 0)
        self.food = self.random_food()

    def run(self):
        while self.running:
            self.clock.tick(144)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.unicode == "+":
                        self.speed = min(144, self.speed + 10)
                        self.move_interval = 1000 // self.speed
                    elif event.unicode == "-":
                        self.speed = max(1, self.speed - 10)
                        self.move_interval = 1000 // self.speed

            self.handle_keys()

            if not self.paused and \
                    current_time - self.last_move_time >= self.move_interval:
                self.move()
                self.last_move_time = current_time

                if self.check_collision():
                    self.reset_game()

            self.draw()

        pygame.quit()
