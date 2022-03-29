try:  # support either PyQt5 or 6
    from PyQt5 import uic
    from PyQt5.QtCore import QModelIndex, QSize, Qt
    from PyQt5.QtGui import QColor, QIcon, QPixmap, QStandardItemModel
    from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
    from PyQt5.QtWidgets import QDialog, QLabel, QTableView, QToolButton

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6 import uic
    from PyQt6.QtCore import QModelIndex, QSize, Qt
    from PyQt6.QtGui import QColor, QIcon, QPixmap, QStandardItemModel
    from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel
    from PyQt6.QtWidgets import QDialog, QTableView, QToolButton

    PyQtVersion = 6

from ColourTable import ColourTable
from ImageDataModel import ImageDataModel


class AssetDialog(QDialog):
    def __init__(self, parent):
        super(AssetDialog, self).__init__(parent)
        uic.loadUi("forms/ChooseAsset.ui", self)
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("assetDatabase.db")
        self.con.open()
        self.asset_name.returnPressed.connect(self.query_database)
        self.cancel_button.clicked.connect(self.close_dialog)
        self.add_button.clicked.connect(self.add_assets)
        self.add_button.setAutoDefault(False)
        self.cancel_button.setAutoDefault(False)
        self.view = None
        self.asset_name.setFocus()

    def query_database(self):
        pass
        print(f"Query {self.asset_name.text()}")
        self.query = ImageDataModel()
        queryColumns = "Name,PerspImage,SideImage,TopImage,FrontImage,AssetID"

        if self.asset_name.text() == "*":
            self.query.setQuery(f"select {queryColumns} from Assets")
        else:
            self.query.setQuery(
                f'select {queryColumns} from Assets where Name like "{self.asset_name.text()}" '
            )
        print(self.query.lastError().text())
        self.view = QTableView(self)
        self.view.setModel(self.query)
        self.view.resizeRowsToContents()
        self.view.resizeColumnsToContents()
        self.grid_layout.addWidget(self.view, 1, 0, 1, 2)
        self.view.show()

    def close_dialog(self):
        self.con.close()
        self.con.removeDatabase("assetDatabase.db")
        self.close()

    def add_assets(self):
        if self.view is not None:
            for index in sorted(self.view.selectionModel().selectedRows()):
                row = index.row()
                image = self.query.data(
                    self.query.index(row, 1), Qt.ItemDataRole.DecorationRole
                )
                name = self.query.data(
                    self.query.index(row, 0), Qt.ItemDataRole.DisplayRole
                )
                database_key = self.query.data(
                    self.query.index(row, 5), Qt.ItemDataRole.DisplayRole
                )
                if database_key not in self.parent().added_assets:
                    img = QPixmap(image)
                    icon = QIcon(img)
                    button = QToolButton()
                    button.setIcon(icon)
                    button.setIconSize(QSize(128, 128))
                    button.setIconSize(QSize(100, 100))
                    new_colour = ColourTable.get_rgb()
                    colour = QColor(new_colour[0], new_colour[1], new_colour[2])
                    button.setProperty("colour", colour)
                    button.setStyleSheet(
                        f"background-color : rgb({colour.red()},{colour.green()},{colour.blue()} ) ; border :5px;"
                    )
                    button.setToolTip(name)
                    button.setProperty("ID", database_key)
                    button.setCheckable(True)
                    button.clicked.connect(self.parent().choose_active_asset)
                    num_widgets = self.parent().asset_layout.count()
                    row = num_widgets / 4
                    col = num_widgets % 4
                    self.parent().asset_layout.addWidget(button, row, col)
                    self.parent().added_assets.append(database_key)
