from PyQt5 import QtWidgets, QtCore, QtGui

class StyledTableWidget(QtWidgets.QTableWidget):
    def __init__(self, table, parent=None):
        super().__init__()
        self.table = table
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("QTableWidget::item { padding: 5px }")
        
    def addData(self, data):
        previous_element = None
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        column_count = self.table.columnCount()
        column_position = 0
        for i in data:
            value = str(i)
            if isinstance(i, float):
                v = str(f"{i:.3f}")
                table_item = QtWidgets.QTableWidgetItem(v)
            else:
                table_item = QtWidgets.QTableWidgetItem(value)
            if len(data) > column_count:
                last_column = self.table.column(previous_element)
                if data.index(i) >= self.table.columnCount():
                    self.table.insertColumn(last_column + 1)

            if i == "Pass":
                table_item.setForeground(QtGui.QColor("green"))
            elif i == "Fail":
                table_item.setForeground(QtGui.QColor("red"))

            self.table.setItem(row_position, column_position, table_item)
            column_position = column_position + 1
            previous_element = table_item
        self.table.resizeRowsToContents()
    
    def addHorizontalHeader(self, header):
        self.table.horizontalHeader().setVisible(True)
        previous_element = None
        column_count = self.table.columnCount()
        column_position = 0
        for i in header:
            _label = str(i)
            header_item = QtWidgets.QTableWidgetItem(_label)
            if len(header) > column_count:
                last_column = self.table.column(previous_element)
                if header.index(i) >= self.table.columnCount():
                    self.table.insertColumn(last_column + 1)

            self.table.setHorizontalHeaderItem(column_position, header_item)
            column_position = column_position + 1
            previous_element = header_item
        self.table.setHorizontalHeaderLabels(header)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet("QHeaderView { font-size: 11pt;" 
                                                    "color: darkblue;}")

    def addVerticalHeader(self, header):
        self.table.verticalHeader().setVisible(True)
        self.table.setVerticalHeaderLabels(header)
        self.table.verticalHeader().setStyleSheet("QHeaderView { font-size: 11pt;" 
                                                    "color: darkblue;}")
