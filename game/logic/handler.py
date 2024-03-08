import random
import math
from typing import List
from game.models import Position, Board, GameObject

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

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

def position_equals(a: Position, b: Position):
    return a.x == b.x and a.y == b.y