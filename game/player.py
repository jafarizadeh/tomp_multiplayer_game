# --------------------------
# FILE: player.py
# Purpose: Defines player attributes and logic
# --------------------------

class Player:
    def __init__(self, player_id, name, start_position):
        """
        Create a new player object.

        Args:
            player_id (str): Unique character identifier (e.g., 'A', 'B')
            name (str): Display name of the player
            start_position (tuple): (row, col) coordinates of initial spawn
        """
        self.id = player_id
        self.name = name
        self.position = start_position  # (row, col)
        self.score = 0
        self.collected_stars = 0

    def move_to(self, new_position):
        """
        Update the player's position.

        Args:
            new_position (tuple): (row, col)
        """
        self.position = new_position

    def add_score(self, amount):
        """
        Increase player's score by a given amount.

        Args:
            amount (int): Score increment
        """
        self.score += amount
        self.collected_stars += amount

    def lose_stars(self, amount):
        """
        Subtract a number of collected stars from the player's score.

        Args:
            amount (int): Number of stars to remove
        """
        self.collected_stars = max(0, self.collected_stars - amount)
        self.score = max(0, self.score - amount)

    def __repr__(self):
        return f"Player(id={self.id}, score={self.score}, pos={self.position})"