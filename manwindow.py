import sys

import win32api
import webbrowser
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QSettings, QTimer
import couart_f_119 as pdf119
from brazer import Window


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.letter_check = " "
        self.banderol_check = " "
        self.parcel_check = " "
        self.recommended_check = " "
        self.price_announcement_check = " "
        self.total_postpaid_check = " "
        self.simpel_check = " "
        self.electron_check = " "
        self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)
        self.saveSetting()
        try:
            self.move(self.settings.value("window position"))
        except:
            pass
        self.l_place_value = self.settings.value("place")
        self.l_place = qtw.QLineEdit(self)
        self.l_place.setMaxLength(14)
        self.l_place.setText(self.l_place_value)
        self.l_date = qtw.QDateTimeEdit(self)
        self.l_date.setCalendarPopup(True)
        self.l_date.setDisplayFormat("dd.MM.yyyy р.")
        self.l_date.setDate(qtc.QDate.currentDate())
        self.l_date.calendarWidget()
        self.l_recipient = qtw.QLineEdit(self)
        self.l_recipient.setMaxLength(103)
        self.l_address = qtw.QLineEdit(self)
        self.l_address.setMaxLength(115)
        self.l_case_number = qtw.QLineEdit(self)
        self.l_case_number.setMaxLength(128)

        self.l_text3_click = qtw.QLabel(self.tr("Найменування адресату*"))
        self.l_text4_click = qtw.QLabel(self.tr("Поштова адреса*"))
        self.l_text5_click = qtw.QLabel(self.tr("Додаткова інформація*    "))

        self.l_name_value = self.settings.value("name")
        self.l_name = qtw.QLabel()
        self.l_name.setText(self.l_name_value)
        self.l_mobil_value = self.settings.value("mobil")
        self.l_mobil = qtw.QLabel()
        self.l_mobil.setText(self.l_mobil_value)
        self.l_address_value = self.settings.value("address")
        self.l_addres = qtw.QLabel()
        self.l_addres.setText(self.l_address_value)

        form_layout = qtw.QFormLayout()
        self.setLayout(form_layout)
        form_layout.addRow("Місце подання", self.l_place)
        form_layout.addRow("Дата подання", self.l_date)
        form_layout.addRow(self.l_text3_click, self.l_recipient)
        form_layout.addRow(self.l_text4_click, self.l_address)
        form_layout.addRow(self.l_text5_click, self.l_case_number)
        form_layout.addRow(qtw.QLabel())

        self.l_text3_click.mouseReleaseEvent = self.showText2
        self.l_text4_click.mouseReleaseEvent = self.showText3
        self.l_text5_click.mouseReleaseEvent = self.showText4

        self.btn_print = qtw.QPushButton("Друк", self)
        self.btn_print.clicked.connect(lambda: self.print_pdf())
        self.btn_print.move(10, 186)
        self.btn_print.resize(100, 26)

        self.btn_preview = qtw.QPushButton("П&ереглянути", self)
        self.btn_preview.clicked.connect(lambda: self.preview_pdf())
        self.btn_preview.move(120, 186)
        self.btn_preview.resize(100, 26)

        self.btn_menu = qtw.QPushButton("Розширене меню", self)
        self.btn_menu.clicked.connect(lambda: self.changeColor())
        self.btn_menu.setStyleSheet(
            "QPushButton:checked {background-color: gray;"
            "border-style: outset;border-width: 2px;border-color: beige;}"
        )
        self.btn_menu.setCheckable(True)
        self.btn_menu.move(305, 186)
        self.btn_menu.resize(100, 26)

        self.btn_adress = qtw.QPushButton("Дані відправника", self)
        self.btn_adress.clicked.connect(lambda: self.show_AnotherWindow())
        self.btn_adress.move(9, 150)
        self.btn_adress.resize(100, 26)
        self.btn_adress.hide()

        self.letter_checkBox = qtw.QCheckBox("Лист", self)
        self.letter_checkBox.move(149, 135)
        self.letter_checkBox.stateChanged.connect(lambda: self.check_box())

        self.banderol_checkBox = qtw.QCheckBox("Бандероль", self)
        self.banderol_checkBox.move(260, 135)
        self.banderol_checkBox.stateChanged.connect(lambda: self.check_box())

        self.parcel_checkBox = qtw.QCheckBox("Посилка", self)
        self.parcel_checkBox.move(347, 135)
        self.parcel_checkBox.stateChanged.connect(lambda: self.check_box())

        self.recommended_checkBox = qtw.QCheckBox("Рекомендоване", self)
        self.recommended_checkBox.move(200, 153)
        self.recommended_checkBox.stateChanged.connect(lambda: self.check_box())

        self.price_announcement_checkBox = qtw.QCheckBox("З оголошеною", self)
        self.price_announcement_checkBox.move(149, 183)
        self.price_announcement_checkBox.hide()
        self.price_announcement = qtw.QLabel(self)
        self.price_announcement.setText("цінністю на")
        self.price_announcement.move(245, 183)
        self.price_announcement.hide()
        self.price_announcement_checkBox.stateChanged.connect(
            lambda: self.stateChange()
        )
        self.price_announcement_checkBox.stateChanged.connect(lambda: self.check_box())

        self.nameprice = qtw.QLabel(self)
        self.nameprice.setText("грн.")
        self.nameprice.move(374, 183)
        self.nameprice.hide()
        self.price = qtw.QLineEdit(self)
        self.price.setMaxLength(7)
        self.price.setEnabled(False)
        self.price.move(308, 189)
        self.price.resize(60, 17)
        self.price.hide()

        self.total_postpaid_checkBox = qtw.QCheckBox("Сума післясплати", self)
        self.total_postpaid_checkBox.move(149, 204)
        self.total_postpaid_checkBox.hide()
        self.total_postpaid_checkBox.stateChanged.connect(lambda: self.stateChange())
        self.total_postpaid_checkBox.stateChanged.connect(lambda: self.check_box())

        self.nametotal = qtw.QLabel(self)
        self.nametotal.setText("грн.")
        self.nametotal.move(374, 207)
        self.nametotal.hide()
        self.total = qtw.QLineEdit(self)
        self.total.setMaxLength(6)
        self.total.setEnabled(False)
        self.total.move(308, 213)
        self.total.resize(60, 17)
        self.total.hide()

        self.nametotal2 = qtw.QLabel(self)
        self.nametotal2.setText("коп.")
        self.nametotal2.move(429, 207)
        self.nametotal2.hide()
        self.total2 = qtw.QLineEdit(self)
        self.total2.setMaxLength(2)
        self.total2.setEnabled(False)
        self.total2.move(400, 213)
        self.total2.resize(25, 17)
        self.total2.hide()

        self.simpel_checkBox = qtw.QCheckBox("Простий", self)
        self.simpel_checkBox.move(149, 225)
        self.simpel_checkBox.hide()
        self.simpel_checkBox.stateChanged.connect(lambda: self.check_box())

        self.electron_checkBox = qtw.QCheckBox("Електронний", self)
        self.electron_checkBox.move(260, 225)
        self.electron_checkBox.hide()
        self.electron_checkBox.stateChanged.connect(lambda: self.check_box())

        self.change_checkBox = qtw.QCheckBox("Інша програма", self)
        self.change_checkBox.move(10, 183)
        self.change_checkBox.hide()
        self.change_checkBox.setToolTip(
            "Поставивши галочку PDF можна\nвідкривати сторонніми програмами"
        )
        self.change_checkBox.setStyleSheet("QCheckBox {font-size: 7pt;}")

        self.off_checkBox = qtw.QCheckBox("Поверх окна", self)
        self.off_checkBox.move(10, 204)
        self.off_checkBox.hide()
        self.off_checkBox.setStyleSheet("QCheckBox {font-size: 7pt;}")
        self.off_checkBox.setToolTip(
            "Поставивши галочку окно перестане\nспливати поверх інших окон"
        )
        self.off_checkBox.stateChanged.connect(
            lambda: self.offChange_over_the_windows()
        )

        self.letter_state = self.settings.value("letter_checkBox", False, type=bool)
        self.letter_checkBox.setChecked(self.letter_state)
        self.letter_checkBox.clicked.connect(lambda: self.saveSetting())

        self.banderol_state = self.settings.value("banderol_checkBox", False, type=bool)
        self.banderol_checkBox.setChecked(self.banderol_state)
        self.banderol_checkBox.clicked.connect(lambda: self.saveSetting())

        self.parcel_state = self.settings.value("parcel_checkBox", False, type=bool)
        self.parcel_checkBox.setChecked(self.parcel_state)
        self.parcel_checkBox.clicked.connect(lambda: self.saveSetting())

        self.recommended_state = self.settings.value(
            "recommended_checkBox", False, type=bool
        )

        self.recommended_checkBox.setChecked(self.recommended_state)
        self.recommended_checkBox.clicked.connect(lambda: self.saveSetting())

        self.change_state = self.settings.value("change_checkBox", False, type=bool)
        self.change_checkBox.setChecked(self.change_state)
        self.change_checkBox.clicked.connect(lambda: self.saveSetting())

        self.off_state = self.settings.value("off_checkBox", False, type=bool)
        self.off_checkBox.setChecked(self.off_state)
        self.off_checkBox.clicked.connect(lambda: self.saveSetting())

    def unhide(self):
        if self.hidden:
            self.price_announcement_checkBox.show()
            self.total_postpaid_checkBox.show()
            self.price_announcement.show()
            self.electron_checkBox.show()
            self.simpel_checkBox.show()
            self.change_checkBox.show()
            self.off_checkBox.show()
            self.nametotal2.show()
            self.nameprice.show()
            self.nametotal.show()
            self.price.show()
            self.total.show()
            self.total2.show()
            self.btn_adress.show()
            self.parcel_checkBox.move(390, 135)
            self.btn_menu.move(353, 265)
            self.btn_print.move(10, 265)
            self.btn_preview.move(120, 265)
            mw.setFixedSize(463, 300)
            mw.update()
            self.hidden = False

    def hide(self):
        self.price_announcement_checkBox.hide()
        self.total_postpaid_checkBox.hide()
        self.price_announcement.hide()
        self.electron_checkBox.hide()
        self.simpel_checkBox.hide()
        self.change_checkBox.hide()
        self.off_checkBox.hide()
        self.nametotal2.hide()
        self.nameprice.hide()
        self.nametotal.hide()
        self.price.hide()
        self.total.hide()
        self.total2.hide()
        self.btn_adress.hide()
        self.parcel_checkBox.move(347, 135)
        self.btn_menu.move(305, 186)
        self.btn_preview.move(120, 186)
        self.btn_print.move(10, 186)
        mw.setFixedSize(415, 220)
        mw.update()
        self.hidden = True

    def changeColor(self):
        self.hidden = True
        if self.btn_menu.isChecked():
            self.unhide()
        else:
            self.hide()

    def make_pdf(self):
        pdf119.make_court_f_119(
            self.l_place.text(),
            self.l_date.text(),
            self.l_recipient.text(),
            self.l_address.text(),
            self.l_case_number.text(),
            self.letter_check,
            self.banderol_check,
            self.parcel_check,
            self.recommended_check,
            self.l_name.text(),
            self.l_mobil.text(),
            self.l_addres.text(),
            self.price_announcement_check,
            self.total_postpaid_check,
            self.simpel_check,
            self.electron_check,
            self.price.text(),
            self.total.text(),
            self.total2.text(),
        )

    def printerPDF(self):
        win32api.ShellExecute(0, "print", "court-f-119.pdf", None, ".", 0)

    def open_(self):
        file_url = r"court-f-119.pdf"
        webbrowser.get("windows-default").open(file_url)

    def preview_pdf(self):
        self.make_pdf()
        self.openChange()

    def print_pdf(self):
        try:
            self.make_pdf()
            self.printerPDF()
            self.timerMessageBox()

        except Exception as ex:
            self.printerPDF()
            self.timerMessageBox()

    def offChange_over_the_windows(self):

        if self.off_checkBox.isChecked():
            self.setWindowFlags(self.windowFlags() & ~qtc.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)
            self.show()

    def openChange(self):
        if self.change_checkBox.isChecked():
            self.open_()
        else:
            self.open_new_Window()

    def check_box(self):
        if self.letter_checkBox.isChecked():
            self.letter_check = "✓"
        else:
            self.letter_check = " "

        if self.banderol_checkBox.isChecked():
            self.banderol_check = "✓"
        else:
            self.banderol_check = " "

        if self.parcel_checkBox.isChecked():
            self.parcel_check = "✓"
        else:
            self.parcel_check = " "

        if self.recommended_checkBox.isChecked():
            self.recommended_check = "✓"
        else:
            self.recommended_check = " "

        if self.price_announcement_checkBox.isChecked():
            self.price_announcement_check = "✓"
        else:
            self.price_announcement_check = " "

        if self.total_postpaid_checkBox.isChecked():
            self.total_postpaid_check = "✓"
        else:
            self.total_postpaid_check = " "

        if self.simpel_checkBox.isChecked():
            self.simpel_check = "✓"
        else:
            self.simpel_check = " "

        if self.electron_checkBox.isChecked():
            self.electron_check = "✓"
        else:
            self.electron_check = " "

    def stateChange(self):
        if self.price_announcement_checkBox.isChecked():
            self.price.setEnabled(True)
        else:
            self.price.setEnabled(False)
            self.price.clear()

        if self.total_postpaid_checkBox.isChecked():
            self.total.setEnabled(True)
            self.total2.setEnabled(True)
        else:
            self.total.setEnabled(False)
            self.total2.setEnabled(False)
            self.total.clear()
            self.total2.clear()

    def saveSetting(self):
        self.settings = QSettings("Main Window", "Win location")
        self.settings_windows1 = QSettings("Main Window", "Web_win location")
        self.settings.sync()

    def closeEvent(self, event):
        self.settings = QSettings("Main Window", "Win location")
        self.settings.setValue("window position", self.pos())
        self.settings.setValue("place", self.l_place.text())
        self.settings.setValue("name", self.l_name.text())
        self.settings.setValue("mobil", self.l_mobil.text())
        self.settings.setValue("address", self.l_addres.text())
        self.settings.setValue("off_checkBox", self.off_checkBox.isChecked())
        self.settings.setValue("change_checkBox", self.change_checkBox.isChecked())
        self.settings.setValue("letter_checkBox", self.letter_checkBox.isChecked())
        self.settings.setValue("banderol_checkBox", self.banderol_checkBox.isChecked())
        self.settings.setValue("parcel_checkBox", self.parcel_checkBox.isChecked())
        self.settings.setValue(
            "recommended_checkBox", self.recommended_checkBox.isChecked()
        )

    def showText2(self, event):
        self.l_recipient.clear()

    def showText3(self, event):
        self.l_address.clear()

    def showText4(self, event):
        self.l_case_number.clear()

    # =================================== open Window ========================================= #

    def open_new_Window(self):
        self._n_window = Window()
        self._n_window.setWindowTitle("Перегляд")
        self._n_window.setWindowIcon(qtg.QIcon("data/Dakirby.ico"))
        self._n_window.setGeometry(420, 50, 800, 420)
        try:
            self._n_window.move(self.settings_windows1.value("web_window position"))
        except:
            pass
        self._n_window.show()

    @qtc.pyqtSlot(str, str, str)
    def update_messages(self, name, mobil, address):

        self.l_name.setText(name)
        self.l_mobil.setText(mobil)
        self.l_addres.setText(address)

    def show_AnotherWindow(self):
        self.dialog = AnotherWindow()
        self.dialog.setWindowIcon(qtg.QIcon("data/Dakirby.ico"))
        self.dialog.submitted.connect(self.update_messages)
        self.dialog.update()
        self.dialog.show()

    def timerMessageBox(self):
        messagebox = TimerMessageBox(3, self)
        messagebox.exec_()


class AnotherWindow(qtw.QDialog):

    submitted = qtc.pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("Main Window", "text")
        self.setWindowTitle("Дані відправника")
        self.setWindowFlag(qtc.Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(349, 123)

        self.l_recipient_name_value = self.settings.value("recipient name")
        self.l_recipient_name = qtw.QLineEdit(self)
        self.l_recipient_name.setMaxLength(47)
        self.l_recipient_name.setText(self.l_recipient_name_value)

        self.l_recipient_mobil_value = self.settings.value("recipient mobil")
        self.l_recipient_mobil = qtw.QLineEdit(self)
        self.l_recipient_mobil.setMaxLength(21)
        self.l_recipient_mobil.setText(self.l_recipient_mobil_value)

        self.l_recipient_address_value = self.settings.value("recipient address")
        self.l_recipient_address = qtw.QLineEdit(self)
        self.l_recipient_address.setMaxLength(93)
        self.l_recipient_address.setText(self.l_recipient_address_value)

        self.l_text_click = qtw.QLabel(self.tr("Найменування відправника*  "))
        self.l_text2_click = qtw.QLabel(self.tr("Номер телефона*"))
        self.l_text3_click = qtw.QLabel(self.tr("Адреса відправника* "))

        form_layout2 = qtw.QFormLayout()
        self.setLayout(form_layout2)
        form_layout2.addRow(self.l_text_click, self.l_recipient_name)
        form_layout2.addRow(self.l_text2_click, self.l_recipient_mobil)
        form_layout2.addRow(self.l_text3_click, self.l_recipient_address)

        self.l_text_click.mouseReleaseEvent = self.showText
        self.l_text2_click.mouseReleaseEvent = self.showText2
        self.l_text3_click.mouseReleaseEvent = self.showText3

        push_btn = qtw.QPushButton("Зберегти", self)
        push_btn.clicked.connect(self.submit)
        push_btn.move(9, 90)
        push_btn.resize(100, 26)

        btn_close = qtw.QPushButton("З&акрити", self)
        btn_close.clicked.connect(lambda: self.close())
        btn_close.move(239, 90)
        btn_close.resize(100, 26)

    def showText(self, event):
        self.l_recipient_name.clear()

    def showText2(self, event):
        self.l_recipient_mobil.clear()

    def showText3(self, event):
        self.l_recipient_address.clear()

    def closeEvent(self, event):
        self.settings = QSettings("Main Window", "text")
        self.settings.setValue("recipient name", self.l_recipient_name.text())
        self.settings.setValue("recipient mobil", self.l_recipient_mobil.text())
        self.settings.setValue("recipient address", self.l_recipient_address.text())

    def set_messages(self, message_name, message_mobil, message_address):
        self.l_recipient_name.setText(message_name)
        self.l_recipient_mobil.setText(message_mobil)
        self.l_recipient_address.setText(message_address)

    def submit(self):
        self.submitted.emit(
            self.l_recipient_name.text(),
            self.l_recipient_mobil.text(),
            self.l_recipient_address.text(),
        )
        self.close()


class TimerMessageBox(qtw.QMessageBox):
    def __init__(self, timeout=0, parent=None):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("Повідомлення")
        self.setWindowIcon(qtg.QIcon("data/Dakirby.ico"))
        self.time_to_wait = timeout
        self.setText("Друк .....".format(timeout))
        self.setStandardButtons(qtw.QMessageBox.Ok)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.setText("Друк .......".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle("Увідомлення")
    mw.setWindowIcon(qtg.QIcon("data/Dakirby.ico"))
    mw.setFixedSize(415, 220)
    mw.update()
    mw.show()
    sys.exit(app.exec_())
