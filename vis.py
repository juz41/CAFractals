#!/usr/bin/env python

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush
from simulation import Simulation, SimulationSetup
from rules import Rules, ClassicRule, RandomRule

class GridWidget(QWidget):
    def __init__(self, sim: Simulation, setup: SimulationSetup):
        super().__init__()
        self.sim = sim
        self.setup = setup
        self._update_cell_colors()

    def _update_cell_colors(self):
        self.cell_colors = {s: self.setup.colors[i] for i, s in enumerate(self.sim.states)} if self.setup.colors else {}

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height = self.width(), self.height()
        # width, height = min(width, height), min(width, height)
        rows, cols = self.sim.size, self.sim.size
        cell_width = width / cols
        cell_height = height / rows

        for y in range(rows):
            for x in range(cols):
                state = self.sim.grid[y, x]
                color_tuple = self.cell_colors.get(state, (100, 100, 100))
                painter.setBrush(QBrush(QColor(*color_tuple)))
                painter.setPen(Qt.GlobalColor.black)
                rect = QRectF(x*cell_width, y*cell_height, cell_width, cell_height)
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        width, height = self.width(), self.height()
        rows, cols = self.sim.size, self.sim.size
        cell_width = width / cols
        cell_height = height / rows
        x = int(event.position().x() // cell_width)
        y = int(event.position().y() // cell_height)
        if 0 <= x < cols and 0 <= y < rows:
            curr_value = self.sim.grid[y, x]
            try:
                idx = self.sim.states.tolist().index(curr_value)
            except ValueError:
                idx = 0
            next_idx = (idx + 1) % self.sim.state_count
            self.sim.grid[y, x] = self.sim.states[next_idx]
            self.update()
            
class SimulationWidget(QWidget):
    def __init__(self, setups):
        super().__init__()
        self.setWindowTitle("Cellular Automaton")
        self.setups = setups
        self.current_setup = list(setups.values())[0]
        self.sim = Simulation(self.current_setup)
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # Grid widget
        self.grid_widget = GridWidget(self.sim, self.current_setup)

        # Controls
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_sim)
        self.step_btn = QPushButton("Step")
        self.step_btn.clicked.connect(self.step_once)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_grid)
        self.random_btn = QPushButton("Randomize")
        self.random_btn.clicked.connect(self.randomize_grid)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(500)
        self.speed_slider.valueChanged.connect(self.change_speed)

        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(3)
        self.grid_size_spin.setMaximum(100)
        self.grid_size_spin.setValue(self.sim.size)
        self.grid_size_spin.valueChanged.connect(self.change_grid_size)

        self.setup_combo = QComboBox()
        for key in setups:
            self.setup_combo.addItem(key)
        self.setup_combo.currentTextChanged.connect(self.change_setup)

        # Layout
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.step_btn)  # Step button
        controls_layout.addWidget(QLabel("Speed"))
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(QLabel("Size"))
        controls_layout.addWidget(self.grid_size_spin)
        controls_layout.addWidget(self.clear_btn)
        controls_layout.addWidget(self.random_btn)
        controls_layout.addWidget(QLabel("Preset"))
        controls_layout.addWidget(self.setup_combo)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.grid_widget)
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)
        self.change_speed()

    def toggle_sim(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            self.timer.start()
            self.start_btn.setText("Stop")

    def step(self):
        self.sim.step()
        self.grid_widget.update()

    def step_once(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        self.sim.step()
        self.grid_widget.update()
        
    def clear_grid(self):
        self.sim.grid.fill(self.sim.states[0])
        self.grid_widget.update()

    def randomize_grid(self):
        self.sim._randomize_grid()
        self.grid_widget.update()

    def change_speed(self):
        interval = max(1, 1001 - self.speed_slider.value())
        self.timer.setInterval(interval)

    def change_grid_size(self, value):
        self.sim.size = value
        self.sim.shape = (value, value)
        self.sim._randomize_grid()
        self.grid_widget.sim = self.sim
        self.grid_widget.update()

    def change_setup(self, name):
        self.current_setup = self.setups[name]
        self.sim = Simulation(self.current_setup)
        self.grid_widget.sim = self.sim
        self.grid_widget.setup = self.current_setup
        self.grid_widget._update_cell_colors()
        self.grid_widget.update()

    def resizeEvent(self, event):
        self.grid_widget.update()  # Stretch grid when window resized

if __name__ == "__main__":
    app = QApplication(sys.argv)

    colors = [(0, 0, 0), (255, 255, 255)]
    game_rules = Rules()
    game_rules.add(ClassicRule(0, 1, True, {1: [3]}))
    game_rules.add(ClassicRule(1, 0, False, {1: [2, 3]}))
    game_setup = SimulationSetup("Game Of Life", n=2, size=10, state_count=2, rules=game_rules, colors=colors, offsets=None)

    random_rules = Rules()
    random_rules.add(RandomRule())
    random_colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
    random_setup = SimulationSetup("Random", n=2, size=10, state_count=3, rules=random_rules, colors=random_colors, offsets=None)

    
    map_colors = [
        (0, 0, 255),
        (255, 255, 150),
        (0, 200, 0),
    ]
    map_rules = Rules()
    map_rules.add(ClassicRule(
        start=0,
        end=1,
        positivity=True,
        values={1: [6, 7, 8]}
    ))
    map_rules.add(ClassicRule(
        start=0,
        end=1,
        positivity=True,
        values={2: [5, 6, 7, 8]}
    ))
    map_rules.add(ClassicRule(
        start=1,
        end=0,
        positivity=True,
        values={0: [5, 6, 7, 8]}
    ))
    map_rules.add(ClassicRule(
        start=1,
        end=2,  
        positivity=True,
        values={1: [5, 6, 7, 8]}
    ))
    map_rules.add(ClassicRule(
        start=1,
        end=2,
        positivity=True,
        values={2: [5, 6, 7, 8]}
    ))
    map_rules.add(ClassicRule(
        start=2,
        end=1,
        positivity=True,
        values={0: [3, 4, 5, 6, 7, 8]}
    ))
    map_rules.add(ClassicRule(
        start=2,
        end=1,
        positivity=True,
        values={1: [4, 5, 6, 7, 8]}
    ))
    map_setup = SimulationSetup(
        "Map",
        n=2,
        size=20,
        state_count=3,
        rules=map_rules,
        colors=map_colors,
        offsets=None,
    )

    setups = {
        "Game Of Life": game_setup,
        "Random": random_setup,
        "Map" : map_setup,
    }

    w = SimulationWidget(setups)
    w.show()
    w.resize(600, 700)
    sys.exit(app.exec())
