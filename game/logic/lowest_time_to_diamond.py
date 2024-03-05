from typing import Tuple
from typing import Optional


from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

import threading
from math import sqrt


class TimeoutException(Exception):  # Custom exception class
    pass

def calculate_path_to_diamond(board_bot: GameObject, board: Board, diamonds: int):
    # Variables
    target = []
    current_position = board_bot.position
    visited_diamonds = set()

    # Find the (5  - current diamonds) the closest diamonds
    while len(target) < 5 - diamonds:
        # Loop reset
        next_diamond = None

        # Find the closest diamond for every diamond
        # limit this to 0.07 seconds

        timer = threading.Timer(board.minimum_delay_between_moves / 1000, lambda: (_ for _ in ()).throw(TimeoutException()))
        timer.start()
        try:
            for diamond in board.diamonds:
                if diamond.properties.points + diamonds > 5:
                    continue

                if diamond.id in visited_diamonds:
                    continue

                if not next_diamond:
                    next_diamond = diamond
                    continue

                if (
                    sqrt(
                        (diamond.position.x - current_position.x) ** 2
                        + (diamond.position.y - current_position.y) ** 2
                    )
                    < sqrt(
                        (next_diamond.position.x - current_position.x) ** 2
                        + (next_diamond.position.y - current_position.y) ** 2
                    )
                ):
                    next_diamond: GameObject = diamond
            if (visited_diamonds is None) or (next_diamond is None):
                break

            visited_diamonds.add(next_diamond.id)
            target.append(next_diamond.position)

        except TimeoutException:
            print(target)
            return target  # If timeout exception is raised, break the loop
        finally:
            timer.cancel()  # stop the timer

    print(target)
    return target


class Main(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    # Calculate the next move
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties

        # Analyze new state
        # If the bot has 5 diamonds, move to the base
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            current_position = board_bot.position
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        #     If the bot has less than 5 diamonds, find the closest diamond
        else:
            # Find atleast 5 - current diamonds in hands
            min_paths = calculate_path_to_diamond(board_bot, board, props.diamonds)
            current_position = board_bot.position
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                min_paths[0].x,
                min_paths[0].y,
            )
        return delta_x, delta_y
