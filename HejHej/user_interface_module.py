from PyQt5 import QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodgeball Measurement App")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(CentralWidget())
        self.show()

class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.velocity_label = QtWidgets.QLabel("Velocity: N/A")
        self.accuracy_label = QtWidgets.QLabel("Accuracy: N/A")
        self.layout().addWidget(self.velocity_label)
        self.layout().addWidget(self.accuracy_label)
        self.start_button = QtWidgets.QPushButton("Start Measurement")
        self.start_button.clicked.connect(self.start_measurement)
        self.layout().addWidget(self.start_button)

    def start_measurement(self):
        # code to start the measurement process
        # ...
        velocity1, velocity2 = data_analysis.calcul
