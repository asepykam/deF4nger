import sys
import re

# Check if PyQt5 module is installed
try:
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QCheckBox
    from PyQt5.QtCore import QTimer, Qt
except ImportError:
    print("PyQt5 module not found. Please install it using 'pip install PyQt5'")
    sys.exit()

def defang(text):
    # Function to defang URLs and IPs
    defanged = text.replace('.', '[.]')
    return defanged

def defang_url_once(text):
    # Function to defang URL once in domain part
    defanged = re.sub(r'(?<=\/\/)(.*?)(\.[^\./]+\.[^\./]+)', lambda m: m.group(1).replace('.', '[.]') + m.group(2), text)
    return defanged

class DeF4ng3rApp(QWidget):
    def __init__(self):
        super().__init__()

        # Create GUI components
        self.clipboard_label = QLabel('Clipboard Content:', self)
        self.clipboard_text = QTextEdit(self)
        self.clipboard_text.setReadOnly(True)

        self.auto_defang_toggle = QCheckBox('Auto Defang', self)
        self.auto_defang_toggle.setChecked(True)

        self.defang_button = QPushButton('Defang Clipboard', self)

        # Set component positions and sizes
        self.clipboard_label.move(10, 10)
        self.clipboard_text.setGeometry(10, 30, 280, 60)

        self.auto_defang_toggle.move(10, 100)

        self.defang_button.setGeometry(10, 130, 280, 30)

        # Create timer to check clipboard every second
        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(1000)

    def check_clipboard(self):
        # Get clipboard content and update text box
        clipboard_text = QApplication.clipboard().text()
        self.clipboard_text.setText(clipboard_text)

        # Check if auto defang is enabled and defang if necessary
        if self.auto_defang_toggle.isChecked():
            # Check if URL has already been defanged
            if '[.]' in clipboard_text:
                return

            defanged_text = defang_url_once(clipboard_text)
            first_dot_index = defanged_text.find('.')
            if first_dot_index != -1:
                defanged_text = defanged_text[:first_dot_index] + '[.]' + defanged_text[first_dot_index + 1:]
            QApplication.clipboard().setText(defanged_text)

    def defang_clipboard(self):
        # Defang clipboard and update text box
        clipboard_text = QApplication.clipboard().text()
        defanged_text = defang(clipboard_text)
        self.clipboard_text.setText(defanged_text)
        QApplication.clipboard().setText(defanged_text)


if __name__ == '__main__':
    # Create QApplication instance and main window
    app = QApplication(sys.argv)
    main_window = DeF4ng3rApp()
    main_window.setGeometry(100, 100, 300, 170)
    main_window.setWindowTitle('DeF4ng3r v0.3')

    # Connect GUI components to functions
    main_window.defang_button.clicked.connect(main_window.defang_clipboard)

    # Show main window and run application
    main_window.show()
    sys.exit(app.exec_())
