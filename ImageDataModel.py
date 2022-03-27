try:  # support either PyQt5 or 6
    from PyQt5.QtCore import Qt, QVariant
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtSql import QSqlQueryModel

    PyQtVersion = 5
except ImportError:
    from PyQt6.QtCore import Qt, QVariant
    from PyQt6.QtGui import QPixmap
    from PyQt6.QtSql import QSqlQueryModel

    PyQtVersion = 6


class ImageDataModel(QSqlQueryModel):
    def __init__(self, parent=None):
        super(QSqlQueryModel, self).__init__(parent)

    def data(self, index, role):
        value = QSqlQueryModel.data(self, index, role)
        # process images these are in columns 1,2,3,4 from our data
        if index.column() in [1, 2, 3, 4]:
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                return QVariant()
            if role == Qt.ItemDataRole.DecorationRole:
                variant = QSqlQueryModel.data(self, index, Qt.ItemDataRole.DisplayRole)
                # img = variant.toByteArray()
                pixmap = QPixmap()
                pixmap.loadFromData(variant, "png")
                return pixmap

        else:
            return value
