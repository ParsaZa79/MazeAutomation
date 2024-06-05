# Maze Game with Pathfinding

## Overview

This project is a Maze Game implemented using PyQt5, which includes pathfinding algorithms such as Backtracking and A*. The game allows users to generate random mazes and visualize the pathfinding process.

## Features

- **Random Maze Generation**: Generate random mazes with adjustable density of blocks.
- **Pathfinding Algorithms**: Visualize pathfinding using Backtracking and A* algorithms.
- **Interactive UI**: User-friendly interface to select algorithms, start pathfinding, and generate new mazes.

## Requirements

- Python 3.x
- PyQt5
- Requests

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```sh
    python main.py
    ```

2. **User Interface**:
    - **Select Algorithm**: Choose between Backtracking and A* algorithms.
    - **Start Pathfinding**: Begin the pathfinding visualization.
    - **Generate Random Map**: Open options to generate a new random maze.

## Code Structure

### main.py

#### Imports

```python
import sys
import random
import heapq
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSlider, QCheckBox, QProgressBar
from PyQt5.QtCore import QTimer, Qt
import threading
import requests
import json
```

#### Constants

```python
WIDTH = 10
HEIGHT = 10
```

#### MazeGame Class

- **`__init__`**: Initializes the UI and sets up variables.
- **`initUI`**: Sets up the user interface.
- **`show_generate_options`**: Displays options for generating a new maze.
- **`generate_map_with_options`**: Generates a maze based on user-selected options.
- **`update_path`**: Updates the UI to show the current path.
- **`select_backtracking`**: Selects the Backtracking algorithm.
- **`select_astar`**: Selects the A* algorithm.
- **`start_pathfinding`**: Starts the pathfinding process.
- **`generate_random_map_normal`**: Generates a random maze without AI.
- **`_generate_random_map_thread_normal`**: Thread function for generating a random maze.
- **`carve_path`**: Ensures a path from start to end in the maze.
- **`generate_random_map_ai`**: Generates a random maze using AI.
- **`_generate_random_map_thread_ai`**: Thread function for generating a random maze using AI.
- **`start_backtracking`**: Initializes variables for Backtracking.
- **`start_astar`**: Initializes variables for A*.
- **`update_visualization`**: Updates the visualization based on the selected algorithm.
- **`backtrack_step`**: Performs a step in the Backtracking algorithm.
- **`astar_step`**: Performs a step in the A* algorithm.
- **`heuristic`**: Heuristic function for A*.

#### Main Function

```python
def main():
    app = QApplication(sys.argv)
    ex = MazeGame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

## Detailed Function Descriptions

### `initUI`

Sets up the main user interface, including the grid layout for the maze, buttons for selecting algorithms, and options for generating new mazes.

### `show_generate_options`

Displays a new window with options for generating a random maze, including a slider for block density and checkboxes for ensuring a path and using AI.

### `generate_map_with_options`

Generates a new maze based on the options selected by the user. It can either use a normal random generation method or an AI-based method.

### `update_path`

Updates the maze grid to show the current path found by the pathfinding algorithm. It colors the path in yellow, the start in green, and the end in red.

### `select_backtracking`

Sets the selected algorithm to Backtracking and updates the UI to reflect the selection.

### `select_astar`

Sets the selected algorithm to A* and updates the UI to reflect the selection.

### `start_pathfinding`

Starts the pathfinding process based on the selected algorithm. It initializes the necessary variables and starts the timer for visualization.

### `generate_random_map_normal`

Generates a random maze without using AI. It places blocks randomly and ensures a path from start to end if required.

### `carve_path`

Ensures there is a path from the start to the end in the maze by using a depth-first search approach.

### `generate_random_map_ai`

Generates a random maze using an AI model. It sends a request to an AI service to generate the maze based on the given parameters.

### `start_backtracking`

Initializes variables for the Backtracking algorithm and starts the timer for visualization.

### `start_astar`

Initializes variables for the A* algorithm and starts the timer for visualization.

### `update_visualization`

Updates the visualization by calling the appropriate step function based on the selected algorithm.

### `backtrack_step`

Performs a single step in the Backtracking algorithm, updating the path and the UI.

### `astar_step`

Performs a single step in the A* algorithm, updating the path and the UI.

### `heuristic`

Heuristic function for the A* algorithm, calculating the Manhattan distance between two points.

---

This documentation guide should help you understand the structure and functionality of the Maze Game with Pathfinding project. If you have any further questions or need additional details, feel free to ask!
