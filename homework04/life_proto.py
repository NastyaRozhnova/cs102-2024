import random
import typing as tp

import pygame
from pygame.locals import QUIT

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_lines()
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []

        for _ in range(self.cell_height):
            row = []
            for _ in range(self.cell_width):
                if randomize:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = 0
                row.append(cell_value)
            grid.append(row)

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        color_white = pygame.Color("white")
        color_green = pygame.Color("green")

        for index, cell_width in enumerate(self.grid):
            y_position = index * self.cell_size
            for j, cell in enumerate(cell_width):
                x_position = j * self.cell_size
                color = color_white if cell == 0 else color_green
                pygame.draw.rect(self.screen, color, (x_position, y_position, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x, y = cell

        x_range = range(max(0, x - 1), min(self.cell_height, x + 2))
        y_range = range(max(0, y - 1), min(self.cell_width, y + 2))

        neib_cells = [self.grid[i][j] for i in x_range for j in y_range if i != x or j != y]

        return neib_cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid()

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                current_cell = self.grid[i][j]
                neighbours = self.get_neighbours((i, j))
                alive_neighbours = sum(neighbours)

                is_cell_alive = current_cell == 1
                will_cell_live = alive_neighbours == 3 or (is_cell_alive and alive_neighbours == 2)

                new_grid[i][j] = 1 if will_cell_live else 0

        return new_grid


if __name__ == "__main__":
    game = GameOfLife(480, 640, 20)
    game.run()
