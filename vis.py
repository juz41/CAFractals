#!/usr/bin/env python

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
import sys

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Hello World - PyQt6")

    layout = QVBoxLayout()
    label = QLabel("Hello, World!")
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
