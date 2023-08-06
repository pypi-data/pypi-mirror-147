import sys, re
try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None

from frontend import *
from PyQt5.QtWidgets import QDialog, QApplication, QTabWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import QSettings, QVariant, Qt, QEvent
from PyQt5.Qt import pyqtSlot, pyqtSignal

from stdcomqt5 import *
from pjanice import  *

