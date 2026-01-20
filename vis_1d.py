#!/usr/bin/env python

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QComboBox, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush

import setups_1d
from simulation import Simulation, SimulationSetup

class GridWidget1D(QWidget):
    def __init__(self, sim: Simulation, setup: SimulationSetup, history, state_count):
        super().__init__()
        self.sim = sim
        self.setup = setup
        self.history = history
        self.state_count = state_count
        self._update_cell_colors()

    def _update_cell_colors(self):
        if getattr(self.setup, "colors", None):
            self.colors = self.setup.colors
        else:
            self.colors = [(150,150,150)] * self.state_count

    def update_history(self, history):
        self.history = history
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height = self.width(), self.height()
        rows, cols = self.history.shape
        if cols == 0 or rows == 0:
            return
        cell_w = width / cols
        cell_h = height / rows
        for r in range(rows):
            for c in range(cols):
                state_idx = int(self.history[r, c])
                color_tuple = self.colors[state_idx] if state_idx < len(self.colors) else (150,150,150)
                painter.setBrush(QBrush(QColor(*color_tuple)))
                painter.setPen(Qt.GlobalColor.black)
                rect = QRectF(c*cell_w, r*cell_h, cell_w, cell_h)
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        width, height = self.width(), self.height()
        rows, cols = self.history.shape
        if cols == 0 or rows == 0:
            return
        cell_w = width / cols
        cell_h = height / rows
        x = int(event.position().x() // cell_w)
        y = int(event.position().y() // cell_h)
        if 0 <= x < cols and 0 <= y < rows:
            curr = int(self.history[y, x])
            nxt = (curr + 1) % self.state_count
            self.history[y, x] = nxt
            if y == rows - 1:
                try:
                    encoded = int(self.sim.states[nxt])
                    self.sim.grid[x] = encoded
                except Exception:
                    pass
            self.update()

class SimulationWidget1D(QWidget):
    def __init__(self, setups_dict):
        super().__init__()
        self.setWindowTitle("1D Cellular Automaton")
        self.setups = setups_dict

        self.width_cells = 101
        self.height_rows = 200

        self.current_setup_name = None
        for k, s in setups_dict.items():
            if getattr(s, "n", None) == 1:
                self.current_setup_name = k
                break
        if self.current_setup_name is None:
            raise RuntimeError("No 1D setup found in setups_dict")
        self.current_setup = setups_dict[self.current_setup_name]

        self.sim = Simulation(self.current_setup, self.width_cells)

        self.state_count = self.sim.state_count
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)

        self._fill_history_from_sim(initial=True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        self.grid_widget = GridWidget1D(self.sim, self.current_setup, self.history, self.state_count)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_sim)
        self.step_btn = QPushButton("Step")
        self.step_btn.clicked.connect(self.step_once)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_history)
        self.random_btn = QPushButton("Randomize")
        self.random_btn.clicked.connect(self.randomize_history)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(500)
        self.speed_slider.valueChanged.connect(self.change_speed)

        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(3)
        self.width_spin.setMaximum(2000)
        self.width_spin.setValue(self.width_cells)
        self.width_spin.valueChanged.connect(self.change_width)

        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(10)
        self.height_spin.setMaximum(2000)
        self.height_spin.setValue(self.height_rows)
        self.height_spin.valueChanged.connect(self.change_height)

        self.wrap_checkbox = QCheckBox("Wrap")
        self.wrap_checkbox.setChecked(False)
        self.wrap_checkbox.stateChanged.connect(self.change_wrap)

        self.setup_combo = QComboBox()
        for key, s in setups_dict.items():
            if getattr(s, "n", None) == 1:
                self.setup_combo.addItem(key)
        self.setup_combo.setCurrentText(self.current_setup_name)
        self.setup_combo.currentTextChanged.connect(self.change_setup)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.step_btn)
        controls_layout.addWidget(QLabel("Speed"))
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(QLabel("Width"))
        controls_layout.addWidget(self.width_spin)
        controls_layout.addWidget(QLabel("Height"))
        controls_layout.addWidget(self.height_spin)
        controls_layout.addWidget(self.wrap_checkbox)
        controls_layout.addWidget(QLabel("Preset"))
        controls_layout.addWidget(self.setup_combo)
        controls_layout.addWidget(self.clear_btn)
        controls_layout.addWidget(self.random_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.grid_widget)
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)

        self.change_speed()

    def _fill_history_from_sim(self, initial=False):
        cols = self.width_cells
        mapper = self.sim.states_dict
        try:
            idxs = np.fromiter((mapper.get(int(v), 0) for v in self.sim.grid.flatten()), dtype=np.uint8)
            idxs = idxs.reshape(-1)
        except Exception:
            idxs = np.zeros(cols, dtype=np.uint8)
            for i, v in enumerate(self.sim.grid.flatten()):
                idxs[i] = mapper.get(int(v), 0)
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        self.history[-1, :cols] = idxs[:cols]
        if hasattr(self, "grid_widget"):
            self.grid_widget.state_count = self.state_count
            self.grid_widget.update_history(self.history)

    def toggle_sim(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            self.timer.start()
            self.start_btn.setText("Stop")

    def step(self):
        self.sim.step()
        self.history[:-1] = self.history[1:]
        mapper = self.sim.states_dict
        last_indices = np.fromiter((mapper.get(int(v), 0) for v in self.sim.grid.flatten()), dtype=np.uint8)
        if last_indices.size < self.width_cells:
            tmp = np.zeros(self.width_cells, dtype=np.uint8)
            tmp[:last_indices.size] = last_indices
            last_indices = tmp
        self.history[-1] = last_indices[:self.width_cells]
        self.grid_widget.update_history(self.history)

    def step_once(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        self.step()

    def clear_history(self, single_seed=False):
        base = self.sim.states[0]
        self.sim.grid.fill(base)
        if single_seed:
            mid = self.width_cells // 2
            if self.sim.state_count > 1:
                self.sim.grid[mid] = self.sim.states[1]
        self._fill_history_from_sim(initial=True)

    def randomize_history(self):
        self.sim._randomize_grid()
        self._fill_history_from_sim()

    def change_speed(self):
        interval = max(1, 1001 - self.speed_slider.value())
        self.timer.setInterval(interval)

    def change_width(self, value):
        old_width = self.width_cells
        old_history = self.history.copy()
        old_sim_grid = self.sim.grid.copy()
        self.width_cells = value
        new_sim = Simulation(self.current_setup, self.width_cells)
        minw = min(old_width, self.width_cells)
        try:
            new_sim.grid[:minw] = old_sim_grid[:minw]
        except Exception:
            pass
        self.sim = new_sim
        self.state_count = self.sim.state_count
        new_history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        minh = min(old_history.shape[0], new_history.shape[0])
        minw = min(old_history.shape[1], new_history.shape[1])
        new_history[:minh, :minw] = old_history[:minh, :minw]
        self.history = new_history
        self.grid_widget.sim = self.sim
        self.grid_widget.setup = self.current_setup
        self.grid_widget.state_count = self.state_count
        self.grid_widget._update_cell_colors()
        self.grid_widget.update_history(self.history)

    def change_height(self, value):
        old = self.history
        self.height_rows = value
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        minh = min(old.shape[0], self.history.shape[0])
        minw = min(old.shape[1], self.history.shape[1])
        self.history[:minh, :minw] = old[:minh, :minw]
        self.grid_widget.update_history(self.history)

    def change_wrap(self, state):
        self.wrap = bool(state == Qt.CheckState.Checked)

    def change_setup(self, name):
        setup = self.setups[name]
        self.current_setup_name = name
        self.current_setup = setup
        self.sim = Simulation(self.current_setup, self.width_cells)
        self.state_count = self.sim.state_count
        self._fill_history_from_sim(initial=True)
        self.grid_widget.sim = self.sim
        self.grid_widget.setup = self.current_setup
        self.grid_widget._update_cell_colors()
        self.grid_widget.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SimulationWidget1D(setups_1d.setups)
    w.show()
    w.resize(900, 700)
    sys.exit(app.exec())
