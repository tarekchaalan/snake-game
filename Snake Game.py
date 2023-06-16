#!/usr/bin/env python3

"""
Snake Eater
Made with PyGame
"""

import sys
import random
import pygame

class Game:
    """
    Snake Eater
    """
    def __init__(self, difficulty):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Snake")

        # Window size
        self.width = 720
        self.height = 480
        self.game_window = pygame.display.set_mode((self.width, self.height))

        # Colors (R, G, B)
        self.colors = {
            "black": pygame.Color(0, 0, 0),
            "white": pygame.Color(255, 255, 255),
            "red": pygame.Color(255, 0, 0),
            "green": pygame.Color(0, 255, 0),
            "blue": pygame.Color(0, 0, 255),
        }

        # Fonts
        self.fonts = {
            "my_font": pygame.font.SysFont("times new roman", 90),
            "leavegame_font": pygame.font.SysFont("times new roman", 30),
            "playagain_font": pygame.font.SysFont("times new roman", 30),
        }

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.difficulty = difficulty
        self.snake = {
            "pos": [100, 50],
            "body": [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]],
        }
        self.food = {
            "pos": [
                random.randint(1, self.width // 10 - 1) * 10,
                random.randint(1, self.height // 10 - 1) * 10,
            ],
            "spawn": True,
        }
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0

    def play_again(self):
        """
        Reset game
        """
        self.snake = {
            "pos": [100, 50],
            "body": [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]],
        }
        self.food = {
            "pos": [
                random.randrange(1, (self.width // 10)) * 10,
                random.randrange(1, (self.height // 10)) * 10,
            ],
            "spawn": True,
        }
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.score = 0

    def show_score(self, choice, color, font, size):
        """
        Displays score on the screen
        """
        score_font = self.fonts[font].render(f"Score: {self.score}", True, color)
        score_rect = score_font.get_rect()
        if choice == 1:
            score_rect.midtop = (self.width / 10, 15)
        else:
            score_rect.midtop = (self.width / 2, self.height / 1.25)
        self.game_window.blit(score_font, score_rect)

    def game_over(self):
        """
        Displays game over message
        """
        game_over_font = self.fonts["my_font"].render("YOU DIED", True, self.colors["red"])
        game_over_rect = game_over_font.get_rect()
        game_over_rect.midtop = (self.width / 2, self.height / 4)

        leavegame_font = self.fonts["leavegame_font"].render(
            "Press ESC to quit", True, self.colors["red"]
        )
        leavegame_rect = leavegame_font.get_rect()
        leavegame_rect.midtop = (self.width / 2, self.height / 1.8)

        playagain_font = self.fonts["playagain_font"].render(
            "Press Space to play again", True, self.colors["green"]
        )
        playagain_rect = playagain_font.get_rect()
        playagain_rect.midtop = (self.width / 2, self.height / 1.5)

        self.game_window.fill(self.colors["black"])
        self.game_window.blit(game_over_font, game_over_rect)
        self.game_window.blit(leavegame_font, leavegame_rect)
        self.game_window.blit(playagain_font, playagain_rect)
        self.show_score(0, self.colors["red"], "times new roman", 20)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.play_again()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            self.fps_controller.tick(self.difficulty)

    def main(self):
        """
        Main game loop
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Whenever a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord("w"):
                        self.change_to = "UP"
                    if event.key == pygame.K_DOWN or event.key == ord("s"):
                        self.change_to = "DOWN"
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.change_to = "LEFT"
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.change_to = "RIGHT"
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Making sure the snake cannot move in the opposite direction instantaneously
            if self.change_to == "UP" and self.direction != "DOWN":
                self.direction = "UP"
            if self.change_to == "DOWN" and self.direction != "UP":
                self.direction = "DOWN"
            if self.change_to == "LEFT" and self.direction != "RIGHT":
                self.direction = "LEFT"
            if self.change_to == "RIGHT" and self.direction != "LEFT":
                self.direction = "RIGHT"

            # Moving the snake
            if self.direction == "UP":
                self.snake["pos"][1] -= 10
            if self.direction == "DOWN":
                self.snake["pos"][1] += 10
            if self.direction == "LEFT":
                self.snake["pos"][0] -= 10
            if self.direction == "RIGHT":
                self.snake["pos"][0] += 10

            # Snake body growing mechanism
            self.snake["body"].insert(0, list(self.snake["pos"]))
            if (
                self.snake["pos"][0] == self.food["pos"][0]
                and self.snake["pos"][1] == self.food["pos"][1]
            ):
                self.score += 1
                self.food["spawn"] = False
            else:
                self.snake["body"].pop()

            # Spawning food on the screen
            if not self.food["spawn"]:
                self.food["pos"] = [
                    random.randrange(1, self.width // 10) * 10,
                    random.randrange(1, self.height // 10) * 10,
                ]

            self.food["spawn"] = True

            # GFX
            self.game_window.fill(self.colors["black"])
            for pos in self.snake["body"]:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(
                    self.game_window, self.colors["green"], pygame.Rect(pos[0], pos[1], 10, 10)
                )

            # Snake food
            pygame.draw.rect(
                self.game_window,
                self.colors["white"],
                pygame.Rect(self.food["pos"][0], self.food["pos"][1], 10, 10),
            )

            # Game Over conditions
            # Getting out of bounds
            if self.snake["pos"][0] < 0:
                self.snake["pos"][0] = self.width - 10
            if self.snake["pos"][0] > self.width - 10:
                self.snake["pos"][0] = 0
            if self.snake["pos"][1] < 0:
                self.snake["pos"][1] = self.height - 10
            if self.snake["pos"][1] > self.height - 10:
                self.snake["pos"][1] = 0
            # Touching the snake body
            for block in self.snake["body"][1:]:
                if self.snake["pos"][0] == block[0] and self.snake["pos"][1] == block[1]:
                    self.game_over()

            self.show_score(1, self.colors["white"], "consolas", 20)
            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            self.fps_controller.tick(self.difficulty)


if __name__ == "__main__":
    DIFFICULTY = int(input("Enter DIFFICULTY (1-120): "))
    if DIFFICULTY > 120:
        print("DIFFICULTY too high, setting to 120")
        DIFFICULTY = 120
    elif DIFFICULTY < 1:
        print("DIFFICULTY too low, setting to 1")
        DIFFICULTY = 1
    game = Game(DIFFICULTY)
    game.main()
