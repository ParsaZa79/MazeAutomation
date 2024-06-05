import sys
import random
import heapq
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSlider, QCheckBox
from PyQt5.QtCore import QTimer, Qt
import threading
from PyQt5.QtWidgets import QProgressBar
import requests
import json

WIDTH = 10
HEIGHT = 10

class MazeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualization)
        self.path = []
        self.visited = set()
        self.stack = []
        self.open_set = []
        self.came_from = {}
        self.g_score = {}
        self.f_score = {}
        self.algorithm = None

    def initUI(self):
        self.setWindowTitle('Maze Game with Pathfinding')
        self.grid_layout = QGridLayout()
        self.buttons = [[QPushButton() for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.maze = [[random.choice([0, 1]) for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.start = (0, 0)
        self.end = (HEIGHT - 1, WIDTH - 1)
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.end[0]][self.end[1]] = 0
    
        for i in range(HEIGHT):
            for j in range(WIDTH):
                btn = self.buttons[i][j]
                btn.setFixedSize(40, 40)
                if self.maze[i][j] == 1:
                    btn.setStyleSheet("background-color: black")
                else:
                    btn.setStyleSheet("background-color: white")
                self.grid_layout.addWidget(btn, i, j)
    
        self.path_label = QLabel("Path: None")
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid_layout)
        self.layout.addWidget(self.path_label)
    
        self.button_layout = QHBoxLayout()
        self.backtracking_button = QPushButton("Select Backtracking")
        self.backtracking_button.clicked.connect(self.select_backtracking)
        self.button_layout.addWidget(self.backtracking_button)
    
        self.astar_button = QPushButton("Select A*")
        self.astar_button.clicked.connect(self.select_astar)
        self.button_layout.addWidget(self.astar_button)
    
        self.start_button = QPushButton("Start Pathfinding")
        self.start_button.clicked.connect(self.start_pathfinding)
        self.button_layout.addWidget(self.start_button)
    
        self.generate_button = QPushButton("Generate Random Map")
        self.generate_button.clicked.connect(self.show_generate_options)
        self.button_layout.addWidget(self.generate_button)
    
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
    
        self.show() 
    
    def show_generate_options(self):
        self.options_window = QWidget()
        self.options_window.setWindowTitle("Generate Map Options")
        layout = QVBoxLayout()
    
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setMinimum(0)
        self.density_slider.setMaximum(100)
        self.density_slider.setValue(30)
        self.density_slider.setTickPosition(QSlider.TicksBelow)
        self.density_slider.setTickInterval(10)
        layout.addWidget(QLabel("Density of Blocks:"))
        layout.addWidget(self.density_slider)
    
        self.ensure_path_checkbox = QCheckBox("Ensure Path from Start to End")
        self.ensure_path_checkbox.setChecked(True)
        layout.addWidget(self.ensure_path_checkbox)
        
        self.generate_with_ai_checkbox = QCheckBox("Generate with AI")
        self.generate_with_ai_checkbox.setChecked(False)
        layout.addWidget(self.generate_with_ai_checkbox)
    
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_map_with_options)
        layout.addWidget(generate_button)
    
        self.options_window.setLayout(layout)
        self.options_window.show()
        
    def generate_map_with_options(self):
        blocks = self.density_slider.value()
        ensure_path = self.ensure_path_checkbox.isChecked()
        with_ai = self.generate_with_ai_checkbox.isChecked()
        
        if with_ai:
            self.generate_random_map_ai(blocks, ensure_path)
        else:
            self.generate_random_map_normal(blocks, ensure_path)
        
        self.options_window.close()
    
    def update_path(self, path):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.maze[i][j] == 1:
                    self.buttons[i][j].setStyleSheet("background-color: black")
                else:
                    self.buttons[i][j].setStyleSheet("background-color: white")
    
        for x, y in path:
            self.buttons[x][y].setStyleSheet("background-color: yellow")
    
        if path:
            self.buttons[self.start[0]][self.start[1]].setStyleSheet("background-color: green")
            self.buttons[self.end[0]][self.end[1]].setStyleSheet("background-color: red")
            
    def select_backtracking(self):
        self.algorithm = "backtracking"
        self.path_label.setText("Algorithm selected: Backtracking")

    def select_astar(self):
        self.algorithm = "astar"
        self.path_label.setText("Algorithm selected: A*")

    def start_pathfinding(self):
        if self.algorithm == "backtracking":
            self.start_backtracking()
        elif self.algorithm == "astar":
            self.start_astar()
        else:
            self.path_label.setText("Please select an algorithm first.")

    def generate_random_map_normal(self, blocks=30, ensure_path=True, max_retries=10):
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.show()

        thread = threading.Thread(target=self._generate_random_map_thread_normal, args=(blocks, ensure_path, max_retries))
        thread.start()

    def _generate_random_map_thread_normal(self, blocks=30, ensure_path=True, max_retries=10):
        for attempt in range(max_retries):
            self.maze = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
            
            # Place blocks randomly
            for _ in range(blocks):
                while True:
                    x, y = random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1)
                    if (x, y) not in [self.start, self.end] and self.maze[x][y] == 0:
                        self.maze[x][y] = 1
                        break
    
            self.maze[self.start[0]][self.start[1]] = 0
            self.maze[self.end[0]][self.end[1]] = 0
    
            if ensure_path:
                if self.carve_path(self.start, self.end):
                    break
            else:
                break
    
        self.update_path([])
        
        self.progress_bar.hide()
    
    def carve_path(self, start, end):
        stack = [start]
        visited = set()
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            x, y = current
            self.maze[x][y] = 0
            if current == end:
                return True
            neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            random.shuffle(neighbors)
            for neighbor in neighbors:
                nx, ny = neighbor
                if 0 <= nx < HEIGHT and 0 <= ny < WIDTH and neighbor not in visited:
                    stack.append(neighbor)
        return False
                    
    def generate_random_map_ai(self, blocks=30, ensure_path=True):
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.show()

        thread = threading.Thread(target=self._generate_random_map_thread_ai, args=(blocks, ensure_path))
        thread.start()

    def _generate_random_map_thread_ai(self, blocks, ensure_path):
        url = "https://inference.friendli.ai/v1/completions"

        payload = json.dumps({
            "model": "mixtral-8x7b-instruct-v0-1",
            "max_tokens": 350,
            "top_k": 1,
            "prompt": f"You are a random maze map generator. You are given a command to generate a random maze map indicating blocks as 1 and empty spaces as 0. You are given a blocks value between 0 and 98, which indicates the number of blocks in the maze. The higher the blocks number the more 1 should be in map. You are also given a boolean value indicating whether to ensure a path from the start to the end. If this value is True, you need to ensure that there is a path from the top-left corner to the bottom-right corner. If this value is False, you can generate a random maze without any constraints.\n The top-left and bottom right cells are always 0. The map is 10x10 in size by default.\nExample 1:\nInput: blocks=14, ensure_path=True\nOutput:\n[0, 1, 0, 0, 1, 0, 0, 0, 0, 0]\n[0, 1, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 1, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 1, 1, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 1, 1, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 1, 0, 0]\n[0, 0, 0, 1, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 1, 0, 0, 0, 1, 0, 0]\n\nExample 2:\nInput: blocks=41, ensure_path=True\nOutput: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 1, 0]\n[0, 1, 1, 1, 1, 1, 1, 0, 1, 0]\n[0, 1, 0, 0, 0, 0, 0, 0, 1, 0]\n[0, 1, 0, 1, 1, 1, 1, 1, 1, 0]\n[0, 1, 0, 1, 0, 0, 0, 0, 0, 0]\n[0, 1, 0, 1, 0, 1, 1, 1, 1, 0]\n[0, 1, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 1, 1, 1, 1, 1, 1, 0]\n\nExample 3:\nInput: blocks=10, ensure_path=False\nOutput:\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 1, 0, 1, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n\nExample 4:\n Input: blocks=63, ensure_path=False\nOutput:\n[0, 0, 0, 0, 0, 1, 1, 1, 1, 1]\n[1, 1, 1, 1, 1, 1, 1, 1, 1, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 1, 0]\n[0, 1, 1, 1, 1, 1, 1, 0, 1, 0]\n[0, 1, 1, 1, 1, 1, 0, 0, 1, 0]\n[0, 1, 1, 1, 1, 1, 1, 1, 1, 0]\n[0, 1, 1, 1, 1, 1, 1, 1, 1, 0]\n[0, 1, 1, 1, 1, 1, 1, 1, 1, 0]\n[0, 1, 0, 0, 0, 0, 1, 1, 0, 0]\n[0, 1, 1, 1, 1, 1, 1, 1, 1, 0]\n\nExample 5:\nInput: blocks=3, ensure_path=True\nOutput:\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n\nWhen given a command just generate a random map based on the given density and ensure_path values. Output only and only the map without any additional text before or after. Now give me the map for Input: blocks={blocks}, ensure_path={ensure_path}"
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer flp_iyWyq5l1GzNFCVLLZWVHUuRjnSb8GkO7hbFCj9Z7CUs7e'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Extract map from response
        response_data = response.json()
        map_text = response_data['choices'][0]['text']

        # Clean anything before '[' and after ']'
        map_text = map_text[map_text.index('['):map_text.rindex(']') + 1]

        map_lines = map_text.strip().split('\n')
        new_maze = []
        for line in map_lines:
            if line.startswith('[') and line.endswith(']'):
                new_maze.append([int(x) for x in line[1:-1].split(',')])

        self.maze = new_maze
        self.update_path([])

        # Hide the progress bar
        self.progress_bar.hide()    

    def start_backtracking(self):
        self.stack = [self.start]
        self.visited = set()
        self.path = []
        self.timer.start(100)

    def start_astar(self):
        self.open_set = []
        heapq.heappush(self.open_set, (0, self.start))
        self.came_from = {}
        self.g_score = {self.start: 0}
        self.f_score = {self.start: self.heuristic(self.start, self.end)}
        self.timer.start(100)

    def update_visualization(self):
        if self.algorithm == "backtracking":
            self.backtrack_step()
        elif self.algorithm == "astar":
            self.astar_step()

    def backtrack_step(self):
        if not self.stack:
            self.timer.stop()
            return
    
        current = self.stack.pop()
        if current in self.visited:
            return
        self.visited.add(current)
        self.path.append(current)
    
        if current == self.end:
            self.timer.stop()
            self.update_path(self.path)
            return
    
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH and self.maze[nx][ny] == 0 and (nx, ny) not in self.visited:
                self.stack.append((nx, ny))
    
        self.update_path(self.path)

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH and self.maze[nx][ny] == 0 and (nx, ny) not in self.visited:
                self.stack.append((nx, ny))

        self.update_path(self.path)

    def astar_step(self):
        if not self.open_set:
            self.timer.stop()
            return
    
        _, current = heapq.heappop(self.open_set)
    
        if current == self.end:
            path = []
            while current in self.came_from:
                path.append(current)
                current = self.came_from[current]
            path.append(self.start)
            self.timer.stop()
            self.update_path(path[::-1])
            return
    
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < HEIGHT and 0 <= neighbor[1] < WIDTH and self.maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = self.g_score[current] + 1
                if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.end)
                    heapq.heappush(self.open_set, (self.f_score[neighbor], neighbor))
    
        self.update_path([current])
        
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

def main():
    app = QApplication(sys.argv)
    ex = MazeGame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
