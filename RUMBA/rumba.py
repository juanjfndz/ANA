import matplotlib.pyplot as plt
import numpy as np
import random


class Casa:
    """
    Represents a procedural generation of a house grid where dirt
    spots are placed.

    Attributes:
        grid_size (tuple): Size of the grid (rows, columns).
        dirt_positions (list): List of coordinates with dirt spots.
    """

    def __init__(self, grid_size=(10, 10), num_dirt_spots=5):
        """
        Initializes the house with a grid and dirt spots.

        Args:
            grid_size (tuple): The size of the grid (rows, columns).
            num_dirt_spots (int): Number of dirt spots to generate
            in the house.
        """
        self.grid_size = grid_size
        self.dirt_positions = self._generate_dirt_spots(num_dirt_spots)

    def _generate_dirt_spots(self, num_dirt_spots):
        """
        Generates random positions for dirt spots within the grid.

        Args:
            num_dirt_spots (int): Number of dirt spots to place.

        Returns:
            list: List of tuples representing dirt spots.
        """
        dirt_spots = []
        for _ in range(num_dirt_spots):
            spot = (random.randint(0, self.grid_size[0] - 1),
                    random.randint(0, self.grid_size[1] - 1))
            if spot not in dirt_spots:  # Ensure no duplicate spots
                dirt_spots.append(spot)
        return dirt_spots

    def get_dirt_positions(self):
        """
        Returns the positions of the dirt spots in the house.

        Returns:
            list: List of coordinates of dirt spots.
        """
        return self.dirt_positions


class Rumba:
    """
    Simulates a Rumba cleaning robot that moves within a defined grid
    and cleans randomly placed dirt spots.

    Attributes:
        position (tuple): Current position of the Rumba in the grid.
        cleaned_spots (list): List of cleaned dirt spots.
    """

    def __init__(self, grid_size=(10, 10), dirt_positions=None):
        """
        Initializes the Rumba with a grid and receives dirt spots to clean.

        Args:
            grid_size (tuple): The size of the grid (rows, columns).
            dirt_positions (list): List of dirt spots provided by the house.
        """
        self.grid_size = grid_size
        self.dirt_positions = dirt_positions if dirt_positions else []
        self.position = (random.randint(0, grid_size[0] - 1),
                         random.randint(0, grid_size[1] - 1))
        self.cleaned_spots = []

    def move(self):
        """
        Moves the Rumba in a random direction (up, down, left, right)
        and cleans dirt if found.
        """
        # Up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        move_dir = random.choice(directions)
        new_position = (self.position[0] + move_dir[0],
                        self.position[1] + move_dir[1])

        # Ensure the Rumba stays within bounds
        new_position = (
            max(0, min(self.grid_size[0] - 1, new_position[0])),
            max(0, min(self.grid_size[1] - 1, new_position[1]))
        )

        self.position = new_position

        # Clean the dirt if present at the new position
        if self.position in self.dirt_positions:
            self.dirt_positions.remove(self.position)
            self.cleaned_spots.append(self.position)

    def is_clean(self):
        """
        Checks if all dirt spots have been cleaned.

        Returns:
            bool: True if all dirt spots are cleaned, False otherwise.
        """
        return len(self.dirt_positions) == 0

    def get_state(self):
        """
        Returns the current state of the Rumba.

        Returns:
            dict: Dictionary with current position, remaining dirt spots,
            and cleaned spots.
        """
        return {
            'position': self.position,
            'dirt_positions': self.dirt_positions,
            'cleaned_spots': self.cleaned_spots
        }


def plot_grid(grid_size, rumba_state):
    """
    Plots the grid with the current state of the Rumba, dirt spots,
    and cleaned spots.

    Args:
        grid_size (tuple): Size of the grid (rows, columns).
        rumba_state (dict): The state of the Rumba with its current position,
        dirt spots, and cleaned spots.
    """
    fig, ax = plt.subplots()

    # Draw grid
    ax.set_xticks(np.arange(0, grid_size[1], 1))
    ax.set_yticks(np.arange(0, grid_size[0], 1))
    ax.grid(True)

    # Mark current position of Rumba
    ax.plot(rumba_state['position'][1], rumba_state['position'][0],
            'bo', label="Rumba", markersize=10)

    # Mark dirt spots
    if rumba_state['dirt_positions']:
        dirt_positions = np.array(rumba_state['dirt_positions'])
        ax.plot(dirt_positions[:, 1], dirt_positions[:, 0], 'ro',
                label="Dirt Spots")

    # Mark cleaned spots
    if rumba_state['cleaned_spots']:
        cleaned_spots = np.array(rumba_state['cleaned_spots'])
        ax.plot(cleaned_spots[:, 1], cleaned_spots[:, 0], 'go',
                label="Cleaned Spots")

    plt.legend()
    plt.xlim(-0.5, grid_size[1] - 0.5)
    plt.ylim(-0.5, grid_size[0] - 0.5)
    plt.gca().invert_yaxis()
    plt.show()


# --- Main simulation loop ---
if __name__ == "__main__":
    grid_size = (10, 10)  # Size of the cleaning area
    num_dirt_spots = 8    # Number of dirt spots

    # Initialize the house (environment)
    casa = Casa(grid_size, num_dirt_spots)

    # Initialize the rumba with dirt spots from the house
    rumba = Rumba(grid_size, casa.get_dirt_positions())

    steps = 0
    max_steps = 100  # Limit the number of steps to avoid infinite loops

    while not rumba.is_clean() and steps < max_steps:
        rumba.move()
        state = rumba.get_state()
        plot_grid(grid_size, state)
        steps += 1

    if rumba.is_clean():
        print(f"All spots cleaned in {steps} steps!")
    else:
        print(f"Rumba could not clean all spots within {max_steps} steps.")
