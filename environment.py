from typing import List
from enum import Enum, auto
import random

class Percept():
    time_step: int
    bump: bool
    breeze: bool
    stench: bool
    scream: bool
    glitter: bool
    reward: int
    done: bool

    def __init__(self, time_step: int, bump: bool, breeze: bool, stench: bool, scream: bool, glitter: bool, reward: int, done: bool):
        # add code to set the instance variables of the percept
        self.time_step = time_step
        self.bump = bump
        self.breeze = breeze
        self.stench = stench
        self.scream = scream
        self.glitter = glitter
        self.reward = reward
        self.done = done


    def __str__(self):
        # add helper function to return the contents of a percept in a readable form
        return (f'time step: {self.time_step} bump: {self.bump} breeze: {self.breeze} stench: {self.stench} scream: {self.scream} glitter: {self.glitter} reward: {self.reward} done: {self.done}')

class Action(Enum):
    LEFT = 0
    RIGHT = 1
    FORWARD = 2
    GRAB = 3
    SHOOT = 4
    CLIMB = 5

class Orientation(Enum):
    E = 0
    S = 1
    W = 2
    N = 3

    def symbol(self) -> str:
        # code for function to return the letter code ("E", "S", etc.) of this instance of an orientation
        # You could create a __str__(self) for this instead of the symbol function if you prefer
        return self.name

    def turn_right(self) -> 'Orientation':
        # return a new orientation turned right
        # Note: the quotes around the type Orientation are because of a quirk in Python.  You can't refer
        # to Orientation without quotes until it is defined (and we are in the middle of defining it)
        new_value = self.value + 1
        if new_value == 4:
            new_value = 0
        return Orientation(new_value)


    def turn_left(self) -> 'Orientation':
        # return a new orientation turned left\
        new_value = self.value - 1
        if new_value == -1:
            new_value = 3
        return Orientation(new_value)

class Location:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'


    def is_left_of(self, location: 'Location')->bool:
        # return True if self is just left of given location
        return True if (self.x == location.x - 1) and (self.y == location.y) else False


    def is_right_of(self, location: 'Location')->bool:
        # return True if self is just right of given location
        return True if (self.x == location.x + 1) and (self.y == location.y) else False


    def is_above(self, location: 'Location')->bool:
        # return True if self is immediately above given location
        return True if (self.x == location.x) and (self.y == location.y + 1) else False


    def is_below(self, location: 'Location')->bool:
        # return True if self is immediately below given location
        return True if (self.x == location.x) and (self.y == location.y - 1) else False


    def neighbours(self)->List['Location']:
        # return list of neighbour locations
        loc_list = []
        # neighbour to the left
        if self.x > 0:
            loc_list.append(Location(self.x - 1, self.y))
        # neighbour to the right
        if self.x < 3:
            loc_list.append(Location(self.x + 1, self.y))
        # neighbour directly below
        if self.y > 0:
            loc_list.append(Location(self.x, self.y - 1))
        # neighbour directly above
        if self.y < 3:
            loc_list.append(Location(self.x, self.y + 1))
        return loc_list




    def is_location(self, location: 'Location')->bool:
        # return True if location given is self's location
        return True if self == location else False


    def at_left_edge(self) -> bool:
        # return True if at the left edge of the grid
        return True if self.x == 0 else False

    def at_right_edge(self) -> bool:
        # return True if at the right edge of the grid
        return True if self.x == 3 else False

    def at_top_edge(self) -> bool:
        # return True if at the top edge of the grid
        return True if self.y == 3 else False

    def at_bottom_edge(self) -> bool:
        # return True if at the bottom edge of the grid
        return True if self.y == 0 else False

    def forward(self, orientation) -> bool:
        # modify self.x and self.y to reflect a forward move and return True if bumped a wall
        # heading west
        if (orientation == 'W') and (self.x > 0):
            self.x -= 1
        elif (orientation == 'W') and (self.x == 0):
            return True
        elif (orientation == 'E') and (self.x < 3):
            self.x += 1
        elif (orientation == 'E') and (self.x == 3):
            return True
        elif (orientation == 'N') and (self.y < 3):
            self.y += 1
        elif (orientation == 'N') and (self.y == 3):
            return True
        elif (orientation == 'S') and (self.y > 0):
            self.y -= 1
        elif (orientation == 'S') and (self.y == 0):
            return True
        return False


    def set_to(self, location: 'Location'):
        # set self.x and self.y to the given location
        self.x = location.x
        self.y = location.y

    @staticmethod
    def from_linear(n: int) -> 'Location':
        # convert an index from 0 to 15 to a location
        row = n // 4
        col = n % 4
        return Location(row, col)

    def to_linear(self)->int:
        # convert self to an index from 0 to 15
        return (self.x * 4 + self.y)

    @staticmethod
    def random() -> 'Location':
        # return a random location
        rand_x = random.randint(0,3)
        rand_y = random.randint(0,3)
        return Location(rand_x, rand_y)

class Environment:
    wumpus_location: Location
    wumpus_alive: bool
    agent_location: Location
    agent_orientation: Orientation
    agent_has_arrow: bool
    agent_has_gold: bool
    game_over: bool
    gold_location: Location
    pit_locations: List[Location]
    time_step: int

    def __init__(self, pit_prob: float, allow_climb_without_gold: bool):
        # initialize the environment state variables (use make functions below)
        self.agent_location = Location(0, 0)
        self.agent_orientation = Orientation['E']
        self.time_step = 0
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.game_over = False
        self.pit_prob = pit_prob
        self.allow_climb_without_gold = allow_climb_without_gold


    def init(self, pit_prob: float, allow_climb_without_gold: bool):
        self.make_wumpus()
        self.make_gold()
        self.make_pits(pit_prob = pit_prob)
        return Percept(self.time_step, False, self.is_breeze(), self.is_stench(), False, self.is_glitter(), 0, False)

    def make_wumpus(self):
        # choose a random location for the wumpus (not bottom left corner) and set it to alive
        rand_x = random.randint(0,3)
        rand_y = random.randint(0,3)
        if (rand_x == 0) and (rand_y == 0):
            self.make_wumpus()
        self.wumpus_alive = True
        self.wumpus_location = Location(rand_x, rand_y)

    def make_gold(self):
        # choose a random location for the gold (not bottom left corner)
        rand_x = random.randint(0,3)
        rand_y = random.randint(0,3)
        if (rand_x == 0) and (rand_y == 0):
            self.make_gold()
        self.gold_location = Location(rand_x, rand_y)

    def make_pits(self, pit_prob: float):
        # create pits with prob pit_prob for all locations except the bottom left corner
        self.pit_locations = []
        for x in range(4):
            for y in range(4):
                if (x == 0) and (y == 0):
                    continue
                prob = random.uniform(0, 1)
                if prob < pit_prob:
                    pit_loc = Location(x, y)
                    self.pit_locations.append(pit_loc)


    def is_pit_at(self, location: Location) -> bool:
        return True if location in self.pit_locations else False

    def is_pit_adjacent_to_agent(self) -> bool:
        # return true if there is a pit above, below, left or right of agent's current location
        for pit_loc in self.pit_locations:
            if (pit_loc.x == self.agent_location.x + 1) and (pit_loc.y == self.agent_location.y):
                return True
            elif (pit_loc.x == self.agent_location.x - 1) and (pit_loc.y == self.agent_location.y):
                return True
            elif (pit_loc.x == self.agent_location.x) and (pit_loc.y == self.agent_location.y - 1):
                return True
            elif (pit_loc.x == self.agent_location.x) and (pit_loc.y == self.agent_location.y + 1):
                return True


    def is_wumpus_adjacent_to_agent(self) -> bool:
        # return true if there is a wumpus adjacent to the agent
        if (self.wumpus_location.x == self.agent_location.x + 1) and (self.wumpus_location.y == self.agent_location.y):
            return True
        elif (self.wumpus_location.x == self.agent_location.x - 1) and (self.wumpus_location.y == self.agent_location.y):
            return True
        elif (self.wumpus_location.x == self.agent_location.x) and (self.wumpus_location.y == self.agent_location.y - 1):
            return True
        elif (self.wumpus_location.x == self.agent_location.x) and (self.wumpus_location.y == self.agent_location.y + 1):
            return True

    def is_agent_at_hazard(self)->bool:
        # return true if the agent is at the location of a pit or the wumpus
        if self.wumpus_location == self.agent_location:
            return True
        for pit_loc in self.pit_locations:
            if pit_loc == self.agent_location:
                return True

    def is_wumpus_at(self, location: Location) -> bool:
        # return true if there is a wumpus at the given location
        return True if self.wumpus_location == location else False


    def is_agent_at(self, location: Location) -> bool:
        # return true if the agent is at the given location
        return True if self.agent_location == location else False

    def is_gold_at(self, location: Location) -> bool:
        # return true if the gold is at the given location
        return True if self.gold_location == location else False

    def is_glitter(self) -> bool:
        # return true if the agent is where the gold is
        return True if self.agent_location == self.gold_location else False

    def is_breeze(self) -> bool:
        # return true if one or pits are adjacent to the agent or the agent is in a room with a pit
        self.is_pit_at(self.agent_location)
        self.is_pit_adjacent_to_agent()
        return False


    def is_stench(self) -> bool:
        # return true if the wumpus is adjacent to the agent or the agent is in the room with the wumpus
        self.is_wumpus_at(self.agent_location)
        self.is_wumpus_adjacent_to_agent()
        return False

    def wumpus_in_line_of_fire(self) -> bool:
        # return true if the wumpus is a cell the arrow would pass through if fired
        if self.agent_orientation == 'W':
            if (self.agent_location.x > self.wumpus_location.x) and (self.agent_location.y == self.wumpus_location.y):
                return True
        elif self.agent_orientation == 'E':
            if (self.agent_location.x < self.wumpus_location.x) and (self.agent_location.y == self.wumpus_location.y):
                return True
        elif self.agent_orientation == 'S':
            if (self.agent_location.x == self.wumpus_location.x) and (self.agent_location.y > self.wumpus_location.y):
                return True
        elif self.agent_orientation == 'N':
            if (self.agent_location.x == self.wumpus_location.x) and (self.agent_location.y < self.wumpus_location.y):
                return True


    def kill_attempt(self) -> bool:
        # return true if the wumpus is alive and in the line of fire
        # if so set the wumpus to dead
        if self.agent_has_arrow and self.wumpus_alive and self.wumpus_in_line_of_fire:
            self.wumpus_alive == False
            return True
        return False

    def step(self, action: Action) -> Percept:
        # for each of the actions, make any agent state changes that result and return a percept including the reward
        # time_step: int, bump: bool, breeze: bool, stench: bool, scream: bool, glitter: bool, reward: int, done: bool
        if self.game_over:
            return Percept(self.time_step, False, False, False, False, False, 0, True)
        else:
            if action == Action['FORWARD']:
                bump = self.agent_location.forward(self.agent_orientation)
                if (self.is_wumpus_at(self.agent_location) and self.wumpus_alive) or self.is_pit_at(self.agent_location):
                    self.game_over = True
                if self.agent_has_gold:
                    self.gold_location = self.agent_location
                self.time_step += 1
                return Percept(self.time_step, bump, self.is_breeze(), self.is_stench(), False, self.is_glitter(), -1 if not self.game_over else -1001, self.game_over)
            elif action == Action['LEFT']:
                self.agent_orientation = self.agent_orientation.turn_left()
                self.time_step += 1
                return Percept(self.time_step, False, self.is_breeze(), self.is_stench(), False, self.is_glitter(), -1, False)
            elif action == Action['RIGHT']:
                self.agent_orientation = self.agent_orientation.turn_right()
                self.time_step += 1
                return Percept(self.time_step, False, self.is_breeze(), self.is_stench(), False, self.is_glitter(), -1, False)
            elif action == Action['GRAB']:
                self.agent_has_gold = True
                self.gold_location = self.agent_location
                self.time_step += 1
                return Percept(self.time_step, False, self.is_breeze(), self.is_stench(), False, True, -1, False)
            elif action == Action['CLIMB']:
                if self.agent_has_gold and (self.agent_location == Location(0,0)):
                    self.game_over = True
                    self.time_step += 1
                    return Percept(self.time_step, False, False, False, False, False, 999, True)
                elif self.allow_climb_without_gold and (self.agent_location == Location(0,0)):
                    self.game_over = True
                    self.time_step += 1
                    return Percept(self.time_step, False, False, False, False, False, -1, True)
                else:
                    self.time_step += 1
                    return Percept(self.time_step, False, self.is_breeze(), self.is_stench(), False, False, 0, False)

            elif action == Action['SHOOT']:
                hadArrow = self.agent_has_arrow
                wumpuskilled = self.kill_attempt()
                self.agent_has_arrow = False
                self.time_step += 1
                return Percept(self.time_step, False, self.is_breeze(), self.is_stench(), wumpuskilled, False, -11 if hadArrow else -1, False)



    # Visualize the game state
    def visualize(self):
        for y in range(3, -1, -1):
            line = '|'
            for x in range(0, 4):
                loc = Location(x, y)
                cell_symbols = [' ', ' ', ' ', ' ']
                if self.is_agent_at(loc): cell_symbols[0] = self.agent_orientation.symbol()
                if self.is_pit_at(loc): cell_symbols[1] = 'P'
                if self.is_wumpus_at(loc):
                    if self.wumpus_alive:
                        cell_symbols[2] = 'W'
                    else:
                        cell_symbols[2] = 'w'
                if self.is_gold_at(loc): cell_symbols[3] = 'G'
                for char in cell_symbols: line += char
                line += '|'
            print(line)
