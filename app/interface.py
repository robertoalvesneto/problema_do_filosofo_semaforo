from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt, QObject, pyqtSignal

from app.controller import PhilosopherActions


class UpdateSignal(QObject):
    update = pyqtSignal()

class PhilosopherTableWindow(QWidget):
    def __init__(self, philosopher_action: PhilosopherActions, stop_philosophers_callback):
        super().__init__()
        self.philosopher_action = philosopher_action
        self.n_philosophers = self.philosopher_action.n_philosophers
        self.stop_philosophers_callback = stop_philosophers_callback

        self.style()
        self.init_ui()
        self.update_signal = UpdateSignal()
        self.update_signal.update.connect(self.update_interface)

        self.setWindowTitle('Problema dos Filósofos')

    def style(self):
        self.style_philosopher_red = "background-color: red; border: 1px solid black; border-radius: 10px;"
        self.style_philosopher_green = "background-color: green; border: 1px solid black; border-radius: 10px;"

        self.style_fork_grey = "background-color: gray; border: 1px solid black; border-radius: 20px;"
        self.style_fork_red = "background-color: red; border: 1px solid black; border-radius: 20px;"

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.grid_interface(main_layout)

        self.counter_interface(main_layout)

        self.setLayout(main_layout)
        self.show()

    def grid_interface(self, main_layout):
        grid_layout = QGridLayout()

        self.philosophers_labels = self.philosophers_icons()

        self.forks_labels = self.forks_icons()

        grid_layout.addWidget(self.forks_labels[0], 0, 1)
        grid_layout.addWidget(self.philosophers_labels[0], 0, 2)
        grid_layout.addWidget(self.forks_labels[1], 0, 3)
        grid_layout.addWidget(self.philosophers_labels[1], 1, 0)
        grid_layout.addWidget(self.philosophers_labels[2], 1, 4)
        grid_layout.addWidget(self.forks_labels[2], 2, 0)
        grid_layout.addWidget(self.philosophers_labels[3], 2, 1)
        grid_layout.addWidget(self.forks_labels[3], 2, 2)
        grid_layout.addWidget(self.philosophers_labels[4], 2, 3)
        grid_layout.addWidget(self.forks_labels[4], 2, 4)

        main_layout.addLayout(grid_layout)

    def philosophers_icons(self):
        philosophers_labels = []
        for i in range(self.n_philosophers):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap('assets/philosopher.png')
            label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            label.setStyleSheet(self.style_philosopher_red)
            philosophers_labels.append(label)

        return philosophers_labels

    def forks_icons(self):
        forks_labels = []
        for i in range(self.n_philosophers):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap('assets/fork.png')
            label.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))
            label.setFixedSize(50, 50)
            label.setStyleSheet(self.style_fork_grey)
            forks_labels.append(label)

        return forks_labels

    def counter_interface(self, main_layout):
        count_layout = QHBoxLayout()
        self.count_philosopher_labels = self.counter_labels()

        for count_label in self.count_philosopher_labels:
            count_layout.addWidget(count_label)

        main_layout.addLayout(count_layout)
    def counter_labels(self):
        count_philosopher_labels = []

        count_meals = self.philosopher_action.count_meals

        for i in range(self.n_philosophers):
            count_philosopher_label = QLabel(f'F {i + 1}: {count_meals[i]}')
            count_philosopher_label.setAlignment(Qt.AlignCenter)
            count_philosopher_labels.append(count_philosopher_label)

        return count_philosopher_labels

    def update_interface(self):
        states = self.philosopher_action.states
        state_forks = self.philosopher_action.state_forks
        count_meals = self.philosopher_action.count_meals

        for i in range(self.n_philosophers):
            if states[i] == "C":
                self.philosophers_labels[i].setStyleSheet(self.style_philosopher_green)
            else:
                self.philosophers_labels[i].setStyleSheet(self.style_philosopher_red)

            if state_forks[i] == "L":
                self.forks_labels[i].setStyleSheet(self.style_fork_grey)
            else:
                self.forks_labels[i].setStyleSheet(self.style_fork_red)

        for i in range(self.n_philosophers):
            self.count_philosopher_labels[i].setText(f'F {i + 1}: {count_meals[i]}')

    def closeEvent(self, event):
        self.stop_philosophers_callback()
        event.accept()