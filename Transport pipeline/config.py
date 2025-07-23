# Network Configuration
GRID_SIZE = (5, 5)                  # Size of the pipe network (width, height)
PIPE_RESISTANCE_RANGE = (1, 10)     # Min/Max resistance values for pipes
ENERGY_PER_UNIT = 0.1               # Energy cost per resistance unit

# Simulation Parameters
SIMULATION_TIME = 100               # Maximum simulation time steps
ANIMATION_FPS = 5                   # Frames per second for output GIF
ANIMATION_DPI = 100                 # Resolution of output animation
FRAME_INTERVAL = 200                # Milliseconds between frames

# Visualization Settings
NODE_SIZE = 800                     # Size of nodes in visualization
NODE_COLOR = "lightgray"            # Base color for nodes
PACKAGE_COLORS = [                  # Colors for different packages
    "red",
    "blue",
    "green",
    "purple",
    "orange"
]
PACKAGE_SIZE = 15                   # Size of package markers
PATH_WIDTH = 2                      # Width of path lines
