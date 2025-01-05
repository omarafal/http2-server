import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QInputDialog, QHBoxLayout, \
    QSplitter
from PyQt5.QtCore import QThread, pyqtSignal
from server_alp import alpn
from alpn_client import alpn_client

class ServerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, log):
        super().__init__()
        self.log = log

    def run(self):
        try:
            alpn(self.log)  # Run server with custom logging
        except Exception as e:
            self.log_signal.emit(f"Server Error: {e}")


class ClientThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, path, log, parent=None):
        super().__init__(parent)
        self.path = path
        self.log = log

    def run(self):
        try:
            alpn_client(self.path, self.log)  # send the path to the client here
        except Exception as e:
            self.log_signal.emit(f"Client Error: {e}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTTP/2 Server and Client GUI")
        self.setGeometry(100, 100, 800, 600)

        # Layout setup
        main_layout = QHBoxLayout()
        splitter = QSplitter()

        # Server section
        server_widget = QWidget()
        server_layout = QVBoxLayout()
        self.server_log_view = QTextEdit()
        self.server_log_view.setReadOnly(True)
        server_layout.addWidget(self.server_log_view)
        self.start_server_button = QPushButton("Start Server")
        self.start_server_button.clicked.connect(self.start_server)
        server_layout.addWidget(self.start_server_button)
        server_widget.setLayout(server_layout)

        # Client section
        client_widget = QWidget()
        client_layout = QVBoxLayout()
        self.client_log_view = QTextEdit()
        self.client_log_view.setReadOnly(True)
        client_layout.addWidget(self.client_log_view)
        self.start_client_button = QPushButton("Start Client")
        self.start_client_button.clicked.connect(self.start_client)
        client_layout.addWidget(self.start_client_button)
        client_widget.setLayout(client_layout)

        # Add widgets to splitter
        splitter.addWidget(server_widget)
        splitter.addWidget(client_widget)

        # Add splitter to main layout
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.server_thread = None
        self.client_thread = None

    def serverlog(self, message):
        self.server_log_view.append(message)

    def clientlog(self, message):
        self.client_log_view.append(message)

    def start_server(self):
        if not self.server_thread or not self.server_thread.isRunning():
            self.server_thread = ServerThread(log=self.serverlog)
            self.server_thread.log_signal.connect(lambda msg: self.serverlog(msg))
            self.server_thread.start()
            self.serverlog("Server started.")
        else:
            self.serverlog("Server is already running.")

    def start_client(self):
        if not self.client_thread or not self.client_thread.isRunning():
            path, ok = QInputDialog.getText(self, "Client Request", "Enter file path:")
            if ok:
                self.client_thread = ClientThread(f"/{path}", log=self.clientlog)
                self.client_thread.log_signal.connect(lambda msg: self.clientlog(msg))
                self.client_thread.start()
                self.clientlog("Client started.")
        else:
            self.clientlog("Client is already running.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
