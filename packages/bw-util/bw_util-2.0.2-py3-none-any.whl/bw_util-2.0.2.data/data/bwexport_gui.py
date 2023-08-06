import logging
import os
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import core
import sys

"""
https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
"""

class QTextEditLogger(QtCore.QObject, logging.Handler):
    appendPlainText = QtCore.pyqtSignal(str)

    def clear(self):
        self.widget.clear()

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        # scroll to bottom
        self.widget.verticalScrollBar().setValue(self.widget.verticalScrollBar().maximum())
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)
        # set to black background
        self.widget.setStyleSheet("background-color: black; color: white;")

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)

    def write(self, msg):
        self.appendPlainText.emit(msg)

# pyqt5 app
class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'BwExport'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.loggingformat =logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        self.initUI()

    def browse_file(self):
        # open file dialog
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')

        self.path_to_file.setText(filename)
        core.bw_path = filename

    def browse_folder(self):
        # open file dialog
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open folder', './')

        self.path_to_folder.setText(folder)
        
    def click_run(self):
        self.run_button.setEnabled(False)
        try:
            # get username and password
            username = self.username.text()
            password = self.password.text()
            # if empty password
            if not password:
                logging.error("password is empty")
                return

            # make folder
            folder = self.path_to_folder.text()
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            # login
            if username:
                logging.info("> login as %s" % username)
                core.login(username, password)

            password_byte = password.encode('utf-8')

            logging.info ("> unlock")
            session = core.unlock(password_byte)
            if session is None:
                logging.error("mac failed")
                return

            # sync
            logging.info("> sync")
            core.sync(password_byte)
            # export
            logging.info("> export")
            core.save_json(password_byte, self.path_to_folder.text())
            core.export(password_byte, self.path_to_folder.text(), session, False)
        except Exception as e:
            logging.error(e)
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # no window resize
        self.setFixedSize(self.size())

        # add browse file button
        self.browse_button = QtWidgets.QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_file)
        # add path to file
        self.path_to_file = QtWidgets.QLineEdit(self)
        self.path_to_file.setText(core.bw_path if core.bw_path else '')
        # disable editing
        self.path_to_file.setReadOnly(True)

        # widget browse button on left path on right
        self.browse_button_layout = QtWidgets.QHBoxLayout()
        self.browse_button_layout.addWidget(self.browse_button)
        self.browse_button_layout.addWidget(self.path_to_file)

        # username input field

        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setText("Username\t")
        #font size
        self.username_label.setFont(QtGui.QFont("Sanserif", 20))

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setFixedHeight(50)

        self.username_layout = QtWidgets.QHBoxLayout()
        self.username_layout.addWidget(self.username_label)
        self.username_layout.addWidget(self.username)

        # password input field
        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText("Password\t")
        self.password_label.setFont(QtGui.QFont("Sanserif", 20))

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setFixedHeight(50)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.password_layout = QtWidgets.QHBoxLayout()
        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password)

        # add run button 
        self.run_button = QtWidgets.QPushButton('Run', self)
        self.run_button.clicked.connect(self.click_run)

        # export path
        self.path_to_folder = QtWidgets.QLineEdit(self)
        self.path_to_folder.setReadOnly(True)
        # get current path
        self.path_to_folder.setText(os.path.join(os.getcwd() + '/export'))
        
        # change folder button
        self.browse_folder_button = QtWidgets.QPushButton('Browse', self)
        self.browse_folder_button.clicked.connect(self.browse_folder)
        

        # add run, export layout
        self.run_layout = QtWidgets.QHBoxLayout()
        self.run_layout.addWidget(self.run_button)
        self.run_layout.addWidget(self.browse_folder_button)
        self.run_layout.addWidget(self.path_to_folder)


        # create stream, logging.basicconfig output to box
        self.logger = QTextEditLogger(self)
        sys.stderr = self.logger
        sys.stdout = self.logger

        self.logger.setFormatter(
            # include function line number
            self.loggingformat
        )
        logging.getLogger().addHandler(self.logger)
        logging.getLogger().setLevel(logging.DEBUG)

        # reset button
        self.reset_button = QtWidgets.QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_run)


        # add layout
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addLayout(self.browse_button_layout)
        self.layout().addLayout(self.username_layout)
        self.layout().addLayout(self.password_layout)
        self.layout().addLayout(self.run_layout)
        self.layout().addWidget(self.logger.widget)
        self.layout().addWidget(self.reset_button)
        # set align center
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.show()

    def reset_run(self):
        self.run_button.setEnabled(True)
        self.username.setText('')
        self.password.setText('')
        self.logger.clear()

def main():
    main = QtWidgets.QApplication(sys.argv)
    app = App()
    sys.exit(main.exec_())

if __name__ == '__main__':
    main = QtWidgets.QApplication(sys.argv)
    app = App()
    sys.exit(main.exec_())