from typing import Tuple
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

import threading
from math import sqrt
import random
from typing import List

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
        #print(last_deposit(props.milliseconds_left,board.minimum_delay_between_moves,board_bot))
        if props.diamonds == 5 or (last_deposit(props.milliseconds_left,board.minimum_delay_between_moves,board_bot) and props.diamonds > 0):
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            current_position = board_bot.position
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
                board
            )
        #     If the bot has less than 5 diamonds, find the closest diamond
        else:
            # Find atleast 5 - current diamonds in hands
            min_paths = calculate_path_to_diamond(board_bot, board, props.diamonds)
            current_position = board_bot.position
            rb = red_button_priority(board,board_bot,min_paths[0].x,min_paths[0].y)
            if rb != 0 :
                min_paths[0] = rb
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                min_paths[0].x,
                min_paths[0].y,
                board,
            )
        return delta_x, delta_y

def last_deposit(time_left,delay, bb : GameObject,):
    base = bb.properties.base
    curr_pos = bb.position
    distance_to_base = abs(base.x - curr_pos.x) + abs(base.y - curr_pos.y)
    time_to_base = delay*distance_to_base*10
    if time_left - time_to_base <=  1000:
        return True
    else:
        return False
    
def red_button_priority(board :Board , bb: GameObject, x,y):
    curr_pos = bb.position
    dd = [dd for dd in board.game_objects if dd.type == "DiamondButtonGameObject"]
    
    rb_pos = dd[0].position
    distance_to_rb = abs(curr_pos.x - rb_pos.x) + abs(curr_pos.y - rb_pos.y)
    distance_to_dia = abs(x-curr_pos.x) + abs(y-curr_pos.y)
    if distance_to_rb < distance_to_dia:
        return rb_pos
    return 0

def isTeleporterAlternatif(current_x, current_y, dest_x, dest_y, teleport_position):
    dest_dist = abs(dest_x- current_x) + abs(dest_y - current_y)
    # calculate distance from current to teleport1
    tele1_dist = abs(teleport_position[0].position.x - current_x) + abs(teleport_position[0].position.y - current_y) + abs(dest_x - teleport_position[1].position.x) + abs(dest_y - teleport_position[1].position.y)
    # calculate distance from current to teleport2
    tele2_dist = abs(teleport_position[1].position.x - current_x) + abs(teleport_position[1].position.y - current_y) + abs(dest_x - teleport_position[0].position.x) + abs(dest_y - teleport_position[0].position.y)

    if(dest_dist < tele1_dist and dest_dist < tele2_dist):
        return False,0
    elif(tele1_dist < tele2_dist):
        return True,1
    else:
        return True,2
    
def isTeleporterInWay(current_x, current_y, dest_x, dest_y, teleport_position):
    if(dest_x > current_x ):
        for i in range(current_x,dest_x + 1):
            if((teleport_position[0].position.x == i and teleport_position[0].position.y == current_y) or (teleport_position[1].position.x == i and teleport_position[1].position.y == current_y)):
                return True
        for i in range(current_y,dest_y + 1):
            if((teleport_position[0].position.y == i and teleport_position[0].position.x == dest_x) or (teleport_position[1].position.y == i and teleport_position[1].position.x == dest_x)):
                return True
    else:
        for i in range(dest_x,current_x + 1):
            if((teleport_position[0].position.x == i and teleport_position[0].position.y == current_y) or (teleport_position[1].position.x == i and teleport_position[1].position.y == current_y)):
                return True
        for i in range(dest_y,current_y + 1):
            if((teleport_position[0].position.y == i and teleport_position[0].position.x == dest_x) or (teleport_position[1].position.y == i and teleport_position[1].position.x == dest_x)):
                return True

def get_direction(current_x, current_y, dest_x, dest_y, board: Board):
    teleport_position : List[GameObject] = get_teleport_position(board)
    isTeleport,teleport_number = isTeleporterAlternatif(current_x, current_y, dest_x, dest_y, teleport_position)

    print(isTeleport,teleport_number)

    delta_x = clamp(dest_x - current_x, -1, 1)
    delta_y = clamp(dest_y - current_y, -1, 1)
    # if the destination is a teleporter
    if(isTeleport):
        print(teleport_number)
        if(teleport_number == 1):
            delta_x = clamp(teleport_position[0].position.x - current_x, -1, 1)
            delta_y = clamp(teleport_position[0].position.y - current_y, -1, 1)
            print("Sampai sini")
            print(delta_x,delta_y)
        else:
            delta_x = clamp(teleport_position[1].position.x - current_x, -1, 1)
            delta_y = clamp(teleport_position[1].position.y - current_y, -1, 1)
            
        
        if delta_x != 0:
            delta_y = 0 
        elif(delta_x == 0 and delta_y == 0):
            rand_choice = random.choice([0,1])
            if(rand_choice == 0):
                delta_y = random.choice([-1,1])
            else:
                delta_x = random.choice([-1,1])
        print("here1")
        return (delta_x, delta_y)
    

    if(not isTeleporterInWay(current_x, current_y, dest_x, dest_y, teleport_position)):
        if delta_x != 0:
            delta_y = 0
        elif(delta_x == 0 and delta_y == 0):
            rand_choice = random.choice([0,1])
            if(rand_choice == 0):
                delta_y = random.choice([-1,1])
            else:
                delta_x = random.choice([-1,1])
        print("here2")
        return (delta_x, delta_y)
        
    else:
        rand_choice = random.randint(0,2)
        if(rand_choice == 0  and delta_x != 0):
            delta_y = 0 
        elif(rand_choice == 1 and delta_y != 0):
            delta_x = 0
        else:
            rand_choice = random.choice([0,1])
            if(rand_choice == 0):
                delta_y = random.choice([-1,1])
                delta_x = 0
            else:
                delta_x = random.choice([-1,1])
                delta_y = 0

        future_positionX,future_positionY = current_x + delta_x, current_y + delta_y
        while((future_positionX == teleport_position[0].position.x and future_positionY == teleport_position[0].position.y) or (future_positionX == teleport_position[1].position.x and future_positionY == teleport_position[1].position.y)):
            if(delta_x == 0):
                delta_x = random.choice([-1,1])
                delta_y = 0
            else:
                delta_y = random.choice([-1,1]) 
                delta_x = 0
            future_positionX,future_positionY = current_x + delta_x, current_y + delta_y      
        print("here3")
        print(delta_x,delta_y)
        return(delta_x,delta_y)
def get_teleport_position(board: Board):
    return [d for d in board.game_objects if d.type == "TeleportGameObject"]

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def position_equals(a: Position, b: Position):
    return a.x == b.x and a.y == b.y