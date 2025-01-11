import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

        self.button = pygame.Rect(0, 0, 150, 50)

        pygame.font.init()
        self.font = pygame.font.SysFont("COMIC SANS MS", 30)

        self.status = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        color_white = pygame.Color("white")
        color_green = pygame.Color("green")

        for index, cell_width in enumerate(self.life.curr_generation):
            y_position = index * self.cell_size
            for j, cell in enumerate(cell_width):
                x_position = j * self.cell_size
                color = color_white if cell == 0 else color_green
                pygame.draw.rect(self.screen, color, (x_position, y_position, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.button.collidepoint(mouse_pos):
                        self.status = not self.status
                    else:
                        if self.status:
                            pos_y = mouse_pos[0] // self.cell_size
                            pos_x = mouse_pos[1] // self.cell_size
                            self.life.curr_generation[pos_x][pos_y] = 1 - self.life.curr_generation[pos_x][pos_y]

            self.draw_grid()
            self.draw_lines()

            if not self.status:
                self.life.step()
                pygame.draw.rect(self.screen, pygame.Color("gray"), self.button, border_radius=8)
                pause_text = self.font.render("pause", True, pygame.Color("black"))
                self.screen.blit(pause_text, (30, 0))
            else:
                pygame.draw.rect(self.screen, pygame.Color("gray"), self.button, border_radius=8)
                resume_text = self.font.render("resume", True, pygame.Color("black"))
                self.screen.blit(resume_text, (30, 0))

            if self.life.is_max_generations_exceeded:
                error_max_generation = self.font.render("Max generations exceeded", True, pygame.Color("red"))
                self.screen.blit(error_max_generation, (self.width // 4, self.height // 2))
            if not self.life.is_changing:
                error_changing = self.font.render("Nothing changing", True, pygame.Color("red"))
                self.screen.blit(error_changing, (self.width // 4, self.height // 2))

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


life = GameOfLife((50, 50), max_generations=500)
ui = GUI(life)
ui.run()
