#!/usr/bin/env python

# ----------------------------
# 3D visualization — drop-in block
# Place this below your Simulation / rules / setups_3d definitions in the same file.
# It will replace the 2D GridWidget/SimulationWidget with 3D versions (same names).
# ----------------------------

import math
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QComboBox, QSpinBox
)
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

from simulation import Simulation, SimulationSetup
from rules import Rules, ClassicRule, RandomRule
import setups

class GridWidget(QOpenGLWidget):
    def __init__(self, sim, setup):
        super().__init__()
        self.sim = sim
        self.setup = setup

        self.cam_rot_x = 30.0
        self.cam_rot_y = -30.0
        self.cam_distance = - (self.sim.size * 2.5)
        self.cam_pan_x = 0.0
        self.cam_pan_y = 0.0

        self._last_pos = None
        self._left_down = False
        self._right_down = False

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._load_colors_from_setup()

    def _load_colors_from_setup(self):
        colors = None
        if hasattr(self.setup, 'colors'):
            colors = getattr(self.setup, 'colors')
        elif isinstance(self.setup, dict) and 'colors' in self.setup:
            colors = self.setup['colors']

        if colors:
            self.cell_colors = {s: (c[0]/255.0, c[1]/255.0, c[2]/255.0) for s,c in zip(self.sim.states, colors)}
        else:
            ramp = np.linspace(0.25, 0.9, self.sim.state_count)
            self.cell_colors = {s: (v,v,v) for s,v in zip(self.sim.states, ramp)}

    # ---------------- OpenGL lifecycle ----------------
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glClearColor(0.08, 0.08, 0.08, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, max(1, h))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w) / max(1.0, h), 0.1, 2000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(self.cam_pan_x, self.cam_pan_y, self.cam_distance)
        glRotatef(self.cam_rot_x, 1.0, 0.0, 0.0)
        glRotatef(self.cam_rot_y, 0.0, 1.0, 0.0)

        self._draw_axes()
        self._draw_voxels()

    def _draw_axes(self):
        glPushMatrix()
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(0.85, 0.2, 0.2); glVertex3f(0,0,0); glVertex3f(2,0,0)
        glColor3f(0.2, 0.85, 0.2); glVertex3f(0,0,0); glVertex3f(0,2,0)
        glColor3f(0.2, 0.2, 0.85); glVertex3f(0,0,0); glVertex3f(0,0,2)
        glEnd()
        glPopMatrix()

    def _draw_voxels(self):
        size = self.sim.size
        grid = self.sim.grid
        glPushMatrix()
        # center the cubic grid at world origin
        glTranslatef(-size/2.0, -size/2.0, -size/2.0)
        half = 0.45  # voxel half-size
        for z in range(size):
            for y in range(size):
                for x in range(size):
                    st = grid[z, y, x]
                    if st == self.sim.states[0]:
                        continue
                    color = self.cell_colors.get(st, (0.6, 0.6, 0.6))
                    glColor4f(color[0], color[1], color[2], 0.1)   # <-- transparency
                    glPushMatrix()
                    glTranslatef(x + 0.5, y + 0.5, z + 0.5)
                    self._draw_cube(half)
                    glPopMatrix()
        glPopMatrix()

    def _draw_cube(self, h):
        glBegin(GL_QUADS)
        # front
        glNormal3f(0,0,1)
        glVertex3f(-h,-h,h); glVertex3f(h,-h,h); glVertex3f(h,h,h); glVertex3f(-h,h,h)
        # back
        glNormal3f(0,0,-1)
        glVertex3f(-h,-h,-h); glVertex3f(-h,h,-h); glVertex3f(h,h,-h); glVertex3f(h,-h,-h)
        # top
        glNormal3f(0,1,0)
        glVertex3f(-h,h,-h); glVertex3f(-h,h,h); glVertex3f(h,h,h); glVertex3f(h,h,-h)
        # bottom
        glNormal3f(0,-1,0)
        glVertex3f(-h,-h,-h); glVertex3f(h,-h,-h); glVertex3f(h,-h,h); glVertex3f(-h,-h,h)
        # right
        glNormal3f(1,0,0)
        glVertex3f(h,-h,-h); glVertex3f(h,h,-h); glVertex3f(h,h,h); glVertex3f(h,-h,h)
        # left
        glNormal3f(-1,0,0)
        glVertex3f(-h,-h,-h); glVertex3f(-h,-h,h); glVertex3f(-h,h,h); glVertex3f(-h,h,-h)
        glEnd()

    # ---------------- interaction ----------------
    def mousePressEvent(self, ev):
        self._last_pos = ev.position()
        self._left_down = bool(ev.buttons() & Qt.MouseButton.LeftButton)
        self._right_down = bool(ev.buttons() & Qt.MouseButton.RightButton)
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._last_pos is None:
            self._last_pos = ev.position()
            return
        dx = ev.position().x() - self._last_pos.x()
        dy = ev.position().y() - self._last_pos.y()

        # left drag rotates unless Ctrl is held -> panning
        if self._left_down and not (ev.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.cam_rot_x += dy * 0.4
            self.cam_rot_y += dx * 0.4
            self.update()
        elif self._right_down or (self._left_down and (ev.modifiers() & Qt.KeyboardModifier.ControlModifier)):
            self.cam_pan_x += dx * 0.01
            self.cam_pan_y -= dy * 0.01
            self.update()

        self._last_pos = ev.position()
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        self._left_down = False
        self._right_down = False
        super().mouseReleaseEvent(ev)

    def wheelEvent(self, ev):
        delta = ev.angleDelta().y() / 120.0
        self.cam_distance += delta * 2.5
        self.update()
        super().wheelEvent(ev)

# ----------------------------
# SimulationWidget: UI with same controls (overwrites your original SimulationWidget)
# ----------------------------
class SimulationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automaton 3D")
        self.setups = setups.setups_3d

        # pick first setup by default
        first_key = next(iter(self.setups.keys()))
        self.current_setup = self.setups[first_key]
        # create sim using your Simulation class: (setup, size)
        self.sim = Simulation(self.current_setup, 16)
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # 3D Grid widget (same attribute name as original code uses)
        self.grid_widget = GridWidget(self.sim, self.current_setup)

        # Controls (match your original layout)
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
        self.grid_size_spin.setMaximum(150)
        self.grid_size_spin.setValue(self.sim.size)
        self.grid_size_spin.valueChanged.connect(self.change_grid_size)

        self.setup_combo = QComboBox()
        for key in self.setups:
            self.setup_combo.addItem(key)
        self.setup_combo.setCurrentText(first_key)
        self.setup_combo.currentTextChanged.connect(self.change_setup)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.step_btn)
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

    # ---------------- control callbacks ----------------
    def toggle_sim(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            self.timer.start()
            self.start_btn.setText("Stop")

    def step(self):
        # call your Simulation.step() — should operate in 3D
        self.sim.step()
        self.grid_widget.update()

    def step_once(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        self.sim.step()
        self.grid_widget.update()

    def clear_grid(self):
        # prefer using your Simulation API if available
        if hasattr(self.sim, 'clear'):
            self.sim.clear()
        else:
            self.sim.grid.fill(self.sim.states[0])
        self.grid_widget.update()

    def randomize_grid(self):
        if hasattr(self.sim, '_randomize_grid'):
            # some of your simulations use private method
            try:
                self.sim._randomize_grid()
            except TypeError:
                # maybe expects a density param
                try:
                    self.sim._randomize_grid(self.sim.random_density)
                except Exception:
                    self.sim.randomize()
        elif hasattr(self.sim, 'randomize'):
            self.sim.randomize()
        else:
            # fallback: random fill first non-zero state
            choices = np.random.rand(self.sim.size, self.sim.size, self.sim.size)
            self.sim.grid = np.where(choices < 0.12, self.sim.states[1], self.sim.states[0]).astype(np.int32)
        self.grid_widget.update()

    def change_speed(self):
        interval = max(1, 1001 - self.speed_slider.value())
        self.timer.setInterval(interval)

    def change_grid_size(self, value):
        # prefer Simulation.resize or setting attributes similar to your original code
        if hasattr(self.sim, 'resize'):
            self.sim.resize(value)
        else:
            # best-effort: replace grid preserving states[0]
            self.sim.size = value
            self.sim.grid = np.full((value, value, value), self.sim.states[0], dtype=np.int32)
            if hasattr(self.sim, '_randomize_grid'):
                try:
                    self.sim._randomize_grid()
                except:
                    pass
        self.grid_widget.sim = self.sim
        self.grid_widget.update()

    def change_setup(self, name):
        self.current_setup = self.setups[name]
        # re-create simulation with same size using your Simulation constructor
        self.sim = Simulation(self.current_setup, self.sim.size)
        self.grid_widget.sim = self.sim
        self.grid_widget.setup = self.current_setup
        self.grid_widget._load_colors_from_setup()
        self.grid_widget.update()

    def resizeEvent(self, event):
        self.grid_widget.update()
        return super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SimulationWidget()
    win.resize(900, 800)
    win.show()
    sys.exit(app.exec())
