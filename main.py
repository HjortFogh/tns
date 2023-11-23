import pygame
import random
from typing import Tuple
import tensorflow as tf
import numpy as np

# Constants
WIDTH, HEIGHT = SCREEN_SIZE = (800, 800)
NUM_COLS, NUM_ROWS = (120, 120)
COL_SIZE, ROW_SIZE = CELL_SIZE = (WIDTH / NUM_COLS, HEIGHT / NUM_ROWS)

Coordinate = Tuple[int, int]
Color = Tuple[int, int, int]

# Pygame setup
pygame.init()

screen =  pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("CodeMath Nexus Studios TM -- The Nexus (TM) Simulation (TN (TM) S) -- Debug version -- All rights reserved (copyright) (TM) (C) --")
pygame.display.set_icon(pygame.image.load("logo.png"))

clock = pygame.time.Clock()

# Draw functions
rect = lambda x, y, w, h, col: pygame.draw.rect(screen, col, (x, y, w, h))

# Utility functions
# def color_hash(key : str) -> Color:
#     hash_val = hash(key)
#     return ((hash_val << 2) % 256, (hash_val << 1) % 256, hash_val % 256)

clamp = lambda val, mn, mx: min(max(val, mn), mx)


def build_model(input_size, output_size):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_dim=input_size),
        tf.keras.layers.Dense(30, activation='sigmoid'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(output_size, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


class Agent:
    def __init__(self, coord : Coordinate) -> None:
        """..."""
        self.coords : Coordinate = coord
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.brain = build_model(2, 2)
    
    def tick(self) -> None:
        #self.coords = (
        #    self.coords[0] + random.randint(-1, 1), 
        #    self.coords[1] + random.randint(-1, 1)
        #    )

        input_data = np.array(self.coords, dtype=float).reshape(1, -1)
        predicted_movement = self.brain.predict(input_data)      

        self.coords += predicted_movement.flatten()

    def show(self) -> None:
        rect(self.coords[0] * COL_SIZE, self.coords[1] * ROW_SIZE, *CELL_SIZE, self.color)

# Main game loop
num_agents = clamp(10, 1, NUM_COLS * NUM_ROWS)
agents = [Agent(coord) for coord in random.sample([(i // NUM_COLS, i % NUM_COLS) for i in range(NUM_COLS * NUM_ROWS)], k=num_agents)]

is_running = True
while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    dt = clock.tick(60)

    screen.fill((70, 70, 70))

    for agent in agents:
        agent.tick()
        agent.show()

    # for x, y in [(i // NUM_COLS, i % NUM_COLS) for i in range(NUM_COLS * NUM_ROWS)]:
    #     pygame.draw.rect(screen, (110, 110, 110), (x * COL_SIZE, y * ROW_SIZE, COL_SIZE, ROW_SIZE), 1)

    pygame.display.flip()

# Quit pygame
pygame.init()