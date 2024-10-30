import pygame  # type: ignore
from constants import (
    WIDTH,
    HEIGHT,
    COLORS,
    FPS,
    COLORS,
    SPOT_HEIGHT,
    SPOT_WIDTH,
    ROWS,
    COLS,
)
from spot import Spot
from typing import List
from algo import make_grid, algorithm
from functools import partial


def draw_grid(surface: pygame.Surface) -> None:
    # Draw horizontal lines
    for row_index in range(ROWS):
        pygame.draw.line(
            surface,
            COLORS["GREY"],
            (0, row_index * SPOT_HEIGHT),
            (COLS * SPOT_WIDTH, row_index * SPOT_HEIGHT),
            width=1,
        )
    # Draw vertical lines
    for col_index in range(COLS):
        pygame.draw.line(
            surface,
            COLORS["GREY"],
            (col_index * SPOT_WIDTH, 0),
            (col_index * SPOT_WIDTH, ROWS * SPOT_HEIGHT),
            width=1,
        )


def draw_spots(surface: pygame.Surface, grid: List[List[Spot]]) -> None:
    for spots in grid:
        for spot in spots:
            spot.draw(surface)


def draw(window, grid, clock):
    draw_spots(surface=window, grid=grid)
    draw_grid(window)
    pygame.display.update()
    clock.tick(FPS)


def pygame_main() -> None:
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Algo Maze Solver")
    clock = pygame.time.Clock()

    running = True
    first = True
    start = None
    end = None
    started = False
    grid: List[List[Spot]] = make_grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # LMB
                x, y = pygame.mouse.get_pos()
                if x < 0 or y < 0 or x > WIDTH and y > HEIGHT:
                    continue
                try:
                    curr_spot: Spot = grid[y // SPOT_HEIGHT][x // SPOT_WIDTH]
                    if not start and not curr_spot.is_end:
                        start = curr_spot
                        curr_spot.make_start()
                    elif not end and not curr_spot.is_start:
                        end = curr_spot
                        curr_spot.make_end()
                    elif curr_spot != start and curr_spot != end:
                        curr_spot.make_barrier()
                except IndexError:
                    continue

            if pygame.mouse.get_pressed()[2]:  # RMB
                x, y = pygame.mouse.get_pos()
                if x < 0 or y < 0 or x > WIDTH and y > HEIGHT:
                    continue
                try:
                    curr_spot: Spot = grid[y // SPOT_HEIGHT][x // SPOT_WIDTH]
                    if curr_spot.is_start:
                        curr_spot.make_free()
                        start = None
                    elif curr_spot.is_end:
                        curr_spot.make_free()
                        end = None
                    elif curr_spot.is_barrier:
                        curr_spot.make_free()
                except IndexError:
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and start and end:
                    started = True
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid=grid)

                    algorithm(partial(draw, window, grid, clock), grid, start, end)

                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    started = False
                    first = True
                    grid = make_grid()

        if first:
            window.fill(COLORS["WHITE"])
            first = False

        draw(window=window, grid=grid, clock=clock)
    pygame.quit()


if __name__ == "__main__":
    pygame_main()
