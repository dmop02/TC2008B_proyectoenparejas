from mesa import Agent
import random
import networkx as nx

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """

        super().__init__(unique_id, model)


    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        x, y = self.pos
        current_cell = self.model.grid.get_cell_list_contents([(x,y)])


        # Flag to check if the traffic light condition is met
        traffic_light_condition_met = False

        # Check if there is a traffic light in the cell
        for agent in current_cell:
            if isinstance(agent, Traffic_Light):
                if not agent.state:
                    # Stop the movement if the traffic light is red
                    return
                else:
                    # Set the flag to indicate that the traffic light condition is met
                    traffic_light_condition_met = True

        # Continue the movement for other agents if the traffic light condition is met
        if traffic_light_condition_met:
            x, y = self.pos
            for agent in current_cell:
                if isinstance(agent, Road):
                    direction = next (agent for agent in current_cell if isinstance(agent, Destination))
                    if direction == "Right":
                        self.model.grid.move_agent(self, (x+1, y))
                    elif direction == "Left":
                        self.model.grid.move_agent(self, (x-1, y))
                    elif direction == "Up":
                        self.model.grid.move_agent(self, (x, y+1))
                    elif direction == "Down":
                        self.model.grid.move_agent(self, (x, y-1))

                
        if any(isinstance(agent, Road)for agent in current_cell):
            road_a = next (agent for agent in current_cell if isinstance(agent, Road))
            if road_a.direction == "Right":
                self.model.grid.move_agent(self, (x+1, y))
            elif road_a.direction == "Left":
                self.model.grid.move_agent(self, (x-1, y))
            elif road_a.direction == "Up":
                self.model.grid.move_agent(self, (x, y+1))
            elif road_a.direction == "Down":
                self.model.grid.move_agent(self, (x, y-1))

        




    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """

        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass