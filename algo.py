from spot import Spot
from typing import List, Callable, Optional, Self
from constants import ROWS, COLS
from queue import PriorityQueue
import pygame  # type: ignore
from dataclasses import dataclass
from functools import total_ordering


# Just python trickery
dummy_spot = Spot(0, 0)


@total_ordering
@dataclass
class AStartQueueItem:
    f_score: float = 0
    count: int = 0
    spot: Spot = dummy_spot

    def __lt__(self, other: Self):
        return (
            self.f_score < other.f_score
            if self.f_score != other.f_score
            else self.count < other.count
        )


def heuristic(spot_a: Spot, spot_b: Spot) -> float:
    return abs(spot_a.x - spot_b.x) + abs(spot_a.y - spot_b.y)


def make_grid() -> List[List[Spot]]:
    grid: List[List[Spot]] = []
    for row_index in range(ROWS):
        row: List[Spot] = []
        for col_index in range(COLS):
            row.append(Spot(row_index, col_index))
        grid.append(row)
    return grid


def algorithm(draw: Callable, grid: List[List[Spot]], start: Spot, end: Spot) -> None:
    count: int = 0
    # PQ structure: dict[float, int, Spot] -> {f_score, count, spot}
    open_set: PriorityQueue = PriorityQueue()
    precursor_of: dict[Spot, Optional[Spot]] = {}
    g_score: dict[Spot, float] = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score: dict[Spot, float] = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start, end)
    open_set.put(AStartQueueItem(0, count, start))
    # To check whether the spot is present in PQ or not
    open_set_hash: set[Spot] = {start}
    while not open_set.empty():
        # Check for the closing of the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current: Spot = open_set.get().spot
        open_set_hash.remove(current)

        if current == end:
            # Make path
            end.make_end()
            current = precursor_of[end]
            while current:
                if current != start:
                    current.make_path()
                    current = precursor_of.get(current)
                    draw()
                else:
                    break
            draw()
            return True

        for neighbor in current.neighbors:
            n_g_score = g_score[current] + 1
            if n_g_score < g_score[neighbor]:
                g_score[neighbor] = n_g_score
                precursor_of[neighbor] = current
                f_score[neighbor] = n_g_score + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put(AStartQueueItem(f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
