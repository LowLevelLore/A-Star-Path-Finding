from constants import SPOT_WIDTH, SPOT_HEIGHT, ROWS, COLS, COLORS
from enum import Enum
from typing import Tuple, List, Self
import pygame  # type: ignore


class SpotState(Enum):
    FREE = 0
    CLOSED = 1
    OPEN = 2
    BARRIER = 3
    START = 4
    END = 5
    PATH = 6


class Spot:
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col
        self.x: int = col * SPOT_WIDTH
        self.y: int = row * SPOT_HEIGHT
        self.state: SpotState = SpotState.FREE
        self.color: Tuple[int, int, int] = COLORS["WHITE"]
        self.neighbors: List[Spot] = []

    @property
    def pos(self) -> Tuple[int, int]:
        return (self.row, self.col)

    @property
    def is_free(self) -> bool:
        return self.state == SpotState.FREE

    @property
    def is_closed(self) -> bool:
        return self.state == SpotState.CLOSED

    @property
    def is_open(self) -> bool:
        return self.state == SpotState.OPEN

    @property
    def is_barrier(self) -> bool:
        return self.state == SpotState.BARRIER

    @property
    def is_start(self) -> bool:
        return self.state == SpotState.START

    @property
    def is_end(self) -> bool:
        return self.state == SpotState.END

    @property
    def is_path(self) -> bool:
        return self.state == SpotState.PATH

    def reset(self) -> None:
        self.state = SpotState.FREE
        self.color = COLORS["WHITE"]

    def make_free(self) -> None:
        self.reset()

    def make_closed(self) -> None:
        self.state = SpotState.CLOSED
        self.color = COLORS["RED"]

    def make_open(self) -> None:
        self.state = SpotState.OPEN
        self.color = COLORS["GREEN"]

    def make_barrier(self) -> None:
        self.state = SpotState.BARRIER
        self.color = COLORS["BLACK"]

    def make_start(self) -> None:
        self.state = SpotState.START
        self.color = COLORS["ORANGE"]

    def make_end(self) -> None:
        self.state = SpotState.END
        self.color = COLORS["TURQUOISE"]

    def make_path(self) -> None:
        self.state = SpotState.PATH
        self.color = COLORS["PURPLE"]

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (self.x, self.y, SPOT_WIDTH, SPOT_HEIGHT))

    def update_neighbors(self, grid: List[List[Self]]) -> None:
        self.neighbors: List[Self] = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier:
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_barrier:
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other: Self):
        return False
