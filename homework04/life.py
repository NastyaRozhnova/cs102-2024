import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []

        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                if randomize:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = 0
                row.append(cell_value)
            grid.append(row)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell

        x_range = range(max(0, x - 1), min(self.rows, x + 2))
        y_range = range(max(0, y - 1), min(self.cols, y + 2))

        neib_cells = [self.curr_generation[i][j] for i in x_range for j in y_range if i != x or j != y]

        return neib_cells

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()

        for i in range(self.rows):
            for j in range(self.cols):
                current_cell = self.curr_generation[i][j]
                neighbours = self.get_neighbours((i, j))
                alive_neighbours = sum(neighbours)

                is_cell_alive = current_cell == 1
                will_cell_live = alive_neighbours == 3 or (is_cell_alive and alive_neighbours == 2)

                new_grid[i][j] = 1 if will_cell_live else 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if self.is_max_generations_exceeded:
            pygame.quit()
            return

        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

        if self.is_changing:
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        cells_changed = self.prev_generation != self.curr_generation
        return cells_changed

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "rb") as f:
            grid = [[int(chr(val)) for val in row if val == 49 or val == 48] for row in f if 49 in row or 48 in row]
        print(grid)
        game = GameOfLife((len(grid), len(grid[0])), randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for line in self.curr_generation:
                line_str = "".join([str(cell) for cell in line])
                f.write(line_str + "\n")
