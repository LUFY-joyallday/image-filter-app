from PyQt5.QtWidgets import QApplication
from gui import ImageFilterApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec_())