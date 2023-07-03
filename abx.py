import sys
import random as r

from audioplayer import AudioPlayer

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QGridLayout
)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ABX Test")

        layout = QGridLayout()

        window_width  = 1000
        window_height = 1000

        # Please insert the pairs of waves here.
        self.waves = [('Chrono 6.mp3', 'Chrono 8.mp3'), ('Chrono 8.mp3', 'Chrono 11.mp3')]

        self.waves_populated = []

        for i in range(10):
            for j in self.waves:
                self.waves_populated.append(j)

        r.shuffle(self.waves_populated)

        for i in range(len(self.waves_populated)):
            print(str(self.waves_populated[i]))
        
        self.i = 0
        self.num_pairs = len(self.waves)
        self.quantity = self.num_pairs * 10

        self.answers = []
        for i in range(self.quantity):
            self.answers.append(r.choice(self.waves_populated[i]))

        self.guesses = [0 for i in range(self.quantity)]

        for i in self.answers:
            print(i)

        self.setGeometry(200, 200, window_width, window_height)

        self.button_x = QPushButton('Play Track X')
        self.button_x.clicked.connect(self.button_x_clicked)

        self.button_a = QPushButton('Play Track A')
        self.button_a.clicked.connect(self.button_a_clicked)

        self.button_b = QPushButton('Play Track B')
        self.button_b.clicked.connect(self.button_b_clicked)

        layout.addWidget(self.button_x, 1, 0)
        layout.addWidget(self.button_a, 2, 0)
        layout.addWidget(self.button_b, 3, 0)

        layout.addWidget(QLabel('Select X = A or B'), 1, 1)

        self.radio_a = QRadioButton('A')
        layout.addWidget(self.radio_a, 2, 1)
        self.radio_a.toggled.connect(self.radio_a_clicked)

        self.radio_b = QRadioButton('B')
        layout.addWidget(self.radio_b, 3, 1)
        self.radio_b.toggled.connect(self.radio_b_clicked)

        self.progress_label = QLabel(str(self.i + 1) + '/' + str(self.quantity))
        layout.addWidget(self.progress_label, 1, 2)

        self.button_next = QPushButton('Next')
        self.button_next.clicked.connect(self.button_next_clicked)
        layout.addWidget(self.button_next, 2, 2)

        self.button_prev = QPushButton('Prev')
        self.button_prev.clicked.connect(self.button_prev_clicked)
        layout.addWidget(self.button_prev, 3, 3)

        self.button_stop = QPushButton('Stop')
        self.button_stop.clicked.connect(self.button_stop_clicked)
        layout.addWidget(self.button_stop, 3, 2)

        self.button_close = QPushButton('Close')
        self.button_close.clicked.connect(self.button_close_clicked)
        layout.addWidget(self.button_close, 1, 3)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        self.audio = AudioPlayer('')

    def radio_a_clicked(self):
        if self.sender().isChecked() and (self.answers[self.i] == self.waves_populated[self.i][0]):
            self.guesses[self.i] = True
        else:
            self.guesses[self.i] = False

    def radio_b_clicked(self):
        if self.sender().isChecked() and (self.answers[self.i] == self.waves_populated[self.i][1]):
            self.guesses[self.i] = True
        else:
            self.guesses[self.i] = False

    def button_x_clicked(self):
        self.audio = AudioPlayer(self.answers[self.i])
        self.audio.play()

    def button_a_clicked(self):
        self.audio = AudioPlayer(self.waves_populated[self.i][0])
        self.audio.play()

    def button_b_clicked(self):
        self.audio = AudioPlayer(self.waves_populated[self.i][1])
        self.audio.play()

    def button_next_clicked(self):
        self.audio.stop()
        self.i += 1
        if self.i == self.quantity:
            self.i = self.quantity -1
            pass
        self.progress_label.setText(str(self.i + 1) + '/' + str(self.quantity))
        
        if self.radio_a.isChecked():
            self.radio_a.setAutoExclusive(False)
            self.radio_a.setChecked(False)
            self.radio_a.setAutoExclusive(True)
        if self.radio_b.isChecked():
            self.radio_b.setAutoExclusive(False)
            self.radio_b.setChecked(False)
            self.radio_b.setAutoExclusive(True)

    def button_prev_clicked(self):
        self.audio.stop()
        self.i -= 1
        if self.i == -1:
            self.i = 0
            pass
        self.progress_label.setText(str(self.i + 1) + '/' + str(self.quantity))

        if self.radio_a.isChecked():
            self.radio_a.setAutoExclusive(False)
            self.radio_a.setChecked(False)
            self.radio_a.setAutoExclusive(True)
        if self.radio_b.isChecked():
            self.radio_b.setAutoExclusive(False)
            self.radio_b.setChecked(False)
            self.radio_b.setAutoExclusive(True)

    def button_stop_clicked(self):
        self.audio.stop()

    def button_close_clicked(self):
        self.write_to_file()
        quit()

    def write_to_file(self):
        with open('Results.txt', 'a') as results:
            results.write('Question Number, Waves, Correct?\n')
            for i in range(len(self.guesses)):
                results.write(str(i + 1) + ': ' + str(self.waves_populated[i]) + ', ' + str(self.guesses[i]) + '\n')

r.seed()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()