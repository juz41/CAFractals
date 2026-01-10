import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QComboBox, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush

import setups
from simulation import SimulationSetup
from rules import RandomRule, Rules

def eca_next_row(rule_number, row, wrap=True):
    """Compute next binary row for elementary CA (3-cell neighborhood)."""
    width = row.size
    next_row = np.zeros_like(row)
    for i in range(width):
        left = row[(i-1)%width] if wrap else (row[i-1] if i-1 >= 0 else 0)
        center = row[i]
        right = row[(i+1)%width] if wrap else (row[i+1] if i+1 < width else 0)
        idx = (left << 2) | (center << 1) | (right)
        bit = (rule_number >> idx) & 1
        next_row[i] = bit
    return next_row

class GridWidget1D(QWidget):
    def __init__(self, history, colors, state_count=2):
        super().__init__()
        self.history = history  # 2D array: rows=time, cols=cells
        self.colors = colors or [(0,0,0),(255,255,255)]
        self.state_count = state_count

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
                state = int(self.history[r, c])
                color_tuple = self.colors[state] if state < len(self.colors) else (150,150,150)
                painter.setBrush(QBrush(QColor(*color_tuple)))
                painter.setPen(Qt.GlobalColor.black)
                rect = QRectF(c*cell_w, r*cell_h, cell_w, cell_h)
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        # obliczamy, która komórka została kliknięta i cyklicznie zmieniamy jej stan
        width, height = self.width(), self.height()
        rows, cols = self.history.shape
        if cols == 0 or rows == 0:
            return
        cell_w = width / cols
        cell_h = height / rows
        # współrzędne kliknięcia
        x = int(event.position().x() // cell_w)
        y = int(event.position().y() // cell_h)
        if 0 <= x < cols and 0 <= y < rows:
            curr = int(self.history[y, x])
            nxt = (curr + 1) % self.state_count
            self.history[y, x] = nxt
            self.update()

class SimulationWidget1D(QWidget):
    def __init__(self, setups_dict):
        super().__init__()
        self.setWindowTitle("1D Cellular Automaton")
        self.setups = setups_dict
        # default params
        self.width_cells = 101
        self.height_rows = 200
        self.rule_number = 30
        self.wrap = True
        self.state_count = 2
        self.colors = [(0,0,0),(255,255,255)]

        # GUI
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # history buffer
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        self.grid_widget = GridWidget1D(self.history, self.colors, self.state_count)  
        # init first row with single center cell
        self.clear_history(single_seed=True)



        # controls
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

        self.rule_spin = QSpinBox()
        self.rule_spin.setMinimum(0)
        self.rule_spin.setMaximum(255)
        self.rule_spin.setValue(self.rule_number)
        self.rule_spin.valueChanged.connect(self.change_rule)

        self.wrap_checkbox = QCheckBox("Wrap")
        self.wrap_checkbox.setChecked(self.wrap)
        self.wrap_checkbox.stateChanged.connect(self.change_wrap)

        self.setup_combo = QComboBox()
        for key, s in setups_dict.items():
            if getattr(s, "n", None) == 1:
                self.setup_combo.addItem(key)
        self.setup_combo.currentTextChanged.connect(self.change_setup)

        # layout
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.step_btn)
        controls_layout.addWidget(QLabel("Speed"))
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(QLabel("Width"))
        controls_layout.addWidget(self.width_spin)
        controls_layout.addWidget(QLabel("Height"))
        controls_layout.addWidget(self.height_spin)
        controls_layout.addWidget(QLabel("Rule"))
        controls_layout.addWidget(self.rule_spin)
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

    def toggle_sim(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            self.timer.start()
            self.start_btn.setText("Stop")

    def step(self):
        # compute next row from last non-empty row (or the bottommost existing row)
        last_row = self.history[-1].copy()
        # if bottom row is all zeros but there exists nonzero earlier, find the last nonzero
        if np.count_nonzero(last_row) == 0:
            nonzeros = np.where(self.history.sum(axis=1) != 0)[0]
            if nonzeros.size > 0:
                last_row = self.history[nonzeros[-1]].copy()
        next_row = eca_next_row(self.rule_number, last_row, wrap=self.wrap)
        # scroll up and append next_row at bottom
        self.history[:-1] = self.history[1:]
        self.history[-1] = next_row
        self.grid_widget.update_history(self.history)

    def step_once(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        self.step()

    def clear_history(self, single_seed=False):
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        if single_seed:
            mid = self.width_cells // 2
            self.history[0, mid] = 1
        self.grid_widget.update_history(self.history)

    def randomize_history(self):
        self.history = np.random.randint(0, self.state_count, size=(self.height_rows, self.width_cells), dtype=np.uint8)
        self.grid_widget.update_history(self.history)

    def change_speed(self):
        interval = max(1, 1001 - self.speed_slider.value())
        self.timer.setInterval(interval)

    def change_width(self, value):
        self.width_cells = value
        old = self.history
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        # copy top-left part
        minh = min(old.shape[0], self.history.shape[0])
        minw = min(old.shape[1], self.history.shape[1])
        self.history[:minh, :minw] = old[:minh, :minw]
        self.grid_widget.update_history(self.history)

    def change_height(self, value):
        self.height_rows = value
        old = self.history
        self.history = np.zeros((self.height_rows, self.width_cells), dtype=np.uint8)
        minh = min(old.shape[0], self.history.shape[0])
        minw = min(old.shape[1], self.history.shape[1])
        self.history[:minh, :minw] = old[:minh, :minw]
        self.grid_widget.update_history(self.history)

    def change_rule(self, val):
        self.rule_number = val

    def change_wrap(self, state):
        self.wrap = bool(state == Qt.CheckState.Checked)

    def change_setup(self, name):
        setup = self.setups[name]
        # use setup colors and state_count if present
        if hasattr(setup, 'colors') and setup.colors:
            self.colors = setup.colors
        if hasattr(setup, 'state_count'):
            self.state_count = setup.state_count
        # update the grid widget palette
        self.grid_widget.colors = self.colors
        self.grid_widget.state_count = self.state_count
        self.grid_widget.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SimulationWidget1D(setups.setups)
    w.show()
    w.resize(900, 700)
    sys.exit(app.exec())
