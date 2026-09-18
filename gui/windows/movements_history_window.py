from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MovementsHistoryWindow(QWidget):
    def __init__(self, movements):
        super().__init__()

        self.movements = movements

        self.setWindowTitle("Storico movimenti")
        self.resize(800, 500)

        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(6)
        self.movements_table.setHorizontalHeaderLabels(
            ["Prodotto", "Data", "Tipo movimento", "Quantità", "Lotto", "Note"]
        )

        self.movements_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.movements_table)

        self.setLayout(layout)

        self.populate_table()

    def populate_table(self):
        for movement in self.movements:
            row = self.movements_table.rowCount()
            self.movements_table.insertRow(row)

            self.movements_table.setItem(
                row, 0, QTableWidgetItem(movement.batch.product.name)
            )
            self.movements_table.setItem(
                row, 1, QTableWidgetItem(str(movement.movement_date))
            )
            self.movements_table.setItem(
                row, 2, QTableWidgetItem(movement.movement_type.value)
            )
            self.movements_table.setItem(
                row, 3, QTableWidgetItem(str(movement.quantity))
            )
            self.movements_table.setItem(
                row, 4, QTableWidgetItem(movement.batch.lot_number or "")
            )
            self.movements_table.setItem(row, 5, QTableWidgetItem(movement.note or ""))
