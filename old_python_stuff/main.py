from PyQt5.QtWidgets import QApplication
from dashboard_window import Dashboard
import sys

def window():
    app = QApplication(sys.argv)
    win = Dashboard()

    # showing window
    win.show()

    ## for clean exit when X is clicked
    sys.exit(app.exec_())

def main():
    window()

if __name__ == "__main__":
    main()