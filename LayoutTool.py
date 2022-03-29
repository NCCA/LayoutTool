#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PyQt5 import uic
    from PyQt5.QtCore import QSize, Qt, QTimer,QPoint
    from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap
    from PyQt5.QtWidgets import QApplication, QDockWidget, QLabel, QMainWindow, QToolBar

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6 import uic
    from PyQt6.QtCore import QPoint, QSize, Qt, QTimer
    from PyQt6.QtGui import QColor, QPainter, QPen, QPixmap
    from PyQt6.QtWidgets import QApplication, QDockWidget, QLabel, QMainWindow, QToolBar

    PyQtVersion = 6

import math
import sys
from enum import Enum
from random import randint, random
from typing import List

from AddAssetDialog import AssetDialog
from lt import app_global


class ZoomMode(Enum):
    In = 1
    Out = 2


class MainWindow(QMainWindow):
    config_settings = app_global.AppGlobal()
    zoom: int = 1
    last_x: int = None
    last_y: int = None
    current_x: int = None
    current_y: int = None
    active_colour: QColor
    spray_timer: QTimer
    added_assets: List[int] = []

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("forms/MainWindow.ui", self)
        # format splitter to correct size
        sizes = [round(self.width() / 0.2), round(self.width() / 0.8)]
        self.main_splitter.setSizes(sizes)
        pixmap = QPixmap(800, 800)
        pixmap.fill(Qt.GlobalColor.white)
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        self.active_colour = QColor(255, 255, 255, 255)
        # self.image_label.setScaledContents(True)
        self.canvas_scroll_area.setWidget(self.image_label)
        self.add_asset.clicked.connect(self.show_add_asset_dialog)
        self.create_paint_toolbar()
        self.spray_timer = QTimer()
        self.spray_timer.timeout.connect(self.update_spray)

    def create_paint_toolbar(self):
        self.brush_toolbox = QDockWidget()
        uic.loadUi("forms/BrushDockWidget.ui", self.brush_toolbox)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.brush_toolbox)

    def mouseMoveEvent(self, event):
        if self.last_x is None:  # First event.
            position = self.image_label.mapFrom(self, event.position() if PyQtVersion ==6 else event.pos())

            self.last_x = position.x()
            self.last_y = position.y()
            return  # Ignore the first time.

        position = self.image_label.mapFrom(self, event.position() if PyQtVersion ==6 else event.pos())
        active_button = (
            self.brush_toolbox.paint_button_group.checkedButton().objectName()
        )

        pixmap = self.image_label.pixmap()
        painter = QPainter(pixmap)

        if active_button == "spray_button":
            # Update the origin for next time.
            self.last_x = position.x()
            self.last_y = position.y()
            self.current_x = position.x()
            self.current_y = position.y()

        elif active_button == "erase_button":
            painter.setPen(
                QPen(QColor(255, 255, 255, 255), self.brush_toolbox.brush_size.value())
            )
        elif active_button == "paint_button":
            painter.setPen(
                QPen(self.active_colour, self.brush_toolbox.brush_size.value())
            )

        painter.drawLine(
            int(self.last_x),
            int(self.last_y),
            int(position.x()),
            int(position.y()),
        )
        painter.end()
        self.image_label.setPixmap(pixmap)
        # Update the origin for next time.
        self.last_x = position.x()
        self.last_y = position.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        if (
            self.brush_toolbox.paint_button_group.checkedButton().objectName()
            == "spray_button"
        ):
            self.spray_timer.stop()

    def mousePressEvent(self, event):
        position = self.image_label.mapFrom(self, event.position() if PyQtVersion ==6 else event.pos())
        self.current_x = position.x()
        self.current_y = position.y()

        if (
            self.brush_toolbox.paint_button_group.checkedButton().objectName()
            == "spray_button"
        ):
            self.spray_timer.start(self.brush_toolbox.spray_speed.value())

    def update_spray(self):
        if (
            self.brush_toolbox.paint_button_group.checkedButton().objectName()
            == "spray_button"
        ):
            pixmap = self.image_label.pixmap()
            painter = QPainter(pixmap)
            painter.setPen(QPen(self.active_colour, 1))
            size = self.brush_toolbox.brush_size.value()

            for i in range(0, 10):
                alpha = 2 * math.pi * random()
                r = size * math.sqrt(random())
                rx = r * math.cos(alpha)
                ry = r * math.sin(alpha)
                painter.drawPoint(
                    QPoint(int(self.current_x + rx), int(self.current_y + ry))
                )
            painter.end()
            self.image_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Escape:
            exit()

    def show_add_asset_dialog(self):
        dialog = AssetDialog(self)
        dialog.show()

    def choose_active_asset(self):
        button = self.sender()
        self.active_colour = button.property("colour")


if __name__ == "__main__":

    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
