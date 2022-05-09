from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QSettings
from PyQt5 import QtCore as qtc


class Window(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super(Window, self).__init__()
        self.settings_windows1 = QSettings("Main Window", "Web_win location")
        try:
            self.move(self.settings_windows1.value("web_window position"))
        except:
            pass
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True
        )
        self.load(qtc.QUrl("file:///court-f-119.pdf"))

    def closeEvent(self, event):
        self.settings_windows1.setValue("web_window position", self.pos())