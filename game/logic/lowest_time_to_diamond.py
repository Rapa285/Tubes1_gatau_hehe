from typing import Tuple
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from .handler import get_direction

import threading
from math import sqrt


class TimeoutException(Exception):  # Custom exception class
    pass


def calculate_path_to_diamond(board_bot: GameObject, board: Board, diamonds: int):
    # Variables
    global temp_next_diamond
    target = []
    current_position = board_bot.position
    visited_diamonds = set()
    timeout_occurred = False  # Add a flag to track if a timeout occurred

    # Find the best path
    while len(target) < 5 - diamonds:
        # Loop reset
        next_diamond = None

        # Find the highest of all diamond acquired / moves
        # limit this to minimum delay seconds

        timer = threading.Timer(1,
                                lambda: (_ for _ in ()).throw(TimeoutException()))
        timer.start()
        try:
            for diamond in board.diamonds:
                if diamond.properties.points + diamonds > 5:
                    continue

                if diamond.id in visited_diamonds:
                    continue

                if not next_diamond:
                    next_diamond = diamond
                    temp_next_diamond = (diamond.properties.points / sqrt((diamond.position.x - current_position.x) ** 2
                                                                          + (
                                                                                      diamond.position.y - current_position.y) ** 2
                                                                          ))
                    continue

                temp_point = (diamond.properties.points /
                              sqrt(
                                  (diamond.position.x - current_position.x) ** 2
                                  + (diamond.position.y - current_position.y) ** 2
                              ))
                if temp_point > temp_next_diamond:
                    next_diamond: GameObject = diamond
                    temp_next_diamond = temp_point

            if (visited_diamonds is None) or (next_diamond is None):
                break

            visited_diamonds.add(next_diamond.id)
            target.append(next_diamond.position)

        except TimeoutException:
            timeout_occurred = True  # Set the flag to True if a timeout occurs
            break  # Break the loop if a timeout occurs
        finally:
            timer.cancel()  # stop the timer

    print(target)
    if timeout_occurred:  # If a timeout occurred, print a message
        print("A timeout occurred during the execution.")
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
                board=board
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
                board=board
            )
        return delta_x, delta_y
