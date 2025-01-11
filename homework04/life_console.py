import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        height, width = screen.getmaxyx()
        i = 1
        while i < height - 1:
            j = 1
            while j < width - 1:
                if i < len(self.life.curr_generation) and j < len(self.life.curr_generation[i]):
                    val = self.life.curr_generation[i][j]
                    ch = " "
                    if val == 1:
                        ch = "1"
                    screen.addch(i, j, ch)
                j += 1
            i += 1

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        running = True

        while running:
            screen.clear()

            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()

            self.life.step()

            if self.life.is_max_generations_exceeded:
                screen.addstr(0, 0, "Max generations exceeded")
                screen.refresh()

            if not self.life.is_changing:
                screen.addstr(0, 0, "Nothing changing")
                screen.refresh()

            key = screen.getch()

            if key == ord("q"):
                running = False
                break

        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((24, 80))
    game = Console(life)
    game.run()
