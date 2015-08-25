__author__ = 'Matjaz'

import sys

import time

from itertools import cycle

from PySide import QtGui, QtCore


# _BEGIN = 'Mon Aug 24 15:32:45 2015'
_BEGIN = time.ctime(time.mktime(time.gmtime()) - time.timezone + 20)

# _INTERVALS = [(2, 'START'), (3, 'Q & A'), (2, 'NEXT')]
_INTERVALS = [(2, 'START'), (8, '__hide__'), (1, 'Q & A'), (10, '__show__'), (2, 'NEXT')]

_GENERATED_LENGTH = 500
_REFRESH_TIME = 500
_WIDTH = 400
_HEIGHT = 180

try:
    with open('timetable.ini', 'rt') as f:
        _BEGIN = f.readline()[:-1]
        _INTERVALS = [(int(x.split('|')[0]), x.split('|')[1][:-1]) for x in f.readlines()]
except FileNotFoundError:
    with open('timetable.ini', 'wt') as f:
        f.write('{0}\n'.format(_BEGIN))
        line_data = [f.write('{0}|{1}\n'.format(val[0], val[1])) for val in _INTERVALS]

class ConferenceTimerWindow(QtGui.QWidget):
    """Main window.
    """
    def __init__(self, desktop, parent=None):
        super(ConferenceTimerWindow, self).__init__(parent=None)

        self.desktop = desktop

        self.setGeometry(self.desktop.width() - _WIDTH, 0, _WIDTH, _HEIGHT)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.4)

        # Main Label.
        self.label = QtGui.QLabel('START')
        self.label.setObjectName('main')
        self.label.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Time Label.
        self.time_label = QtGui.QLabel('')
        self.time_label.setObjectName('time')
        self.time_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.worker)
        self.timer.start(_REFRESH_TIME)

        # Main layout.
        main_layout = QtGui.QHBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.time_label)

        self.setLayout(main_layout)
        with open('style.qss', 'rt') as f:
            self.setStyleSheet(f.read())

        ### Generate times
        self.begin = time.mktime(time.strptime(_BEGIN))
        rtime = self.begin

        iter_intervals = cycle(_INTERVALS)
        self.time_list = []
        self.key_list = []

        for i in range(_GENERATED_LENGTH):
            interval, key = iter_intervals.__next__()
            self.time_list.append(rtime)
            self.key_list.append(key)
            rtime += interval

    def worker(self):
        """Checks if there is any work, every second."""
        # Calculate current time (seconds since ...).
        current_time = time.mktime(time.gmtime()) - time.timezone

        # Update clock.
        # self.time_label.setText(time.ctime(current_time))
        self.time_label.setText(time.strftime('%H:%M', time.localtime()))

        if current_time < self.begin:
            self.label.setText('ICoEV 2015')
        else:
            # Updage msg.
            last = len([0 for i in self.time_list if i < current_time]) - 1
            if last < 0:
                pass
            else:
                key = self.key_list[last]

                if '__hide__' in key:
                    self.hide()
                elif '__show__' in key:
                    self.show()
                else:
                    self.label.setText(key)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main_window = ConferenceTimerWindow(app.desktop())
    main_window.show()

    sys.exit(app.exec_())