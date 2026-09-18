from PySide6.QtWidgets import (
    QAbstractItemView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ExpiringProductsWindow(QWidget):
    def __init__(self, expired, expiring):
        super().__init__()

        self.expired = expired
        self.expiring = expiring

        self.setWindowTitle("Scadenze")
        self.resize(700, 500)

        self.expired_label = QLabel("Prodotti scaduti")

        self.expired_table = QTableWidget()
        self.expired_table.setColumnCount(5)
        self.expired_table.setHorizontalHeaderLabels(
            ["Prodotto", "Quantità", "Scadenza", "Lotto", "Posizione"]
        )
        self.expired_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.expiring_label = QLabel("Prodotti in scandeza entro 30 giorni")

        self.expiring_table = QTableWidget()
        self.expiring_table.setColumnCount(5)
        self.expiring_table.setHorizontalHeaderLabels(
            ["Prodotto", "Quantità", "Scadenza", "Lotto", "Posizione"]
        )
        self.expiring_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()

        layout.addWidget(self.expired_label)
        layout.addWidget(self.expired_table)
        layout.addWidget(self.expiring_label)
        layout.addWidget(self.expiring_table)

        self.setLayout(layout)

        self.populate_table()

    def populate_table(self):
        for batch in self.expired:
            row = self.expired_table.rowCount()
            self.expired_table.insertRow(row)

            self.expired_table.setItem(row, 0, QTableWidgetItem(batch.product.name))
            self.expired_table.setItem(row, 1, QTableWidgetItem(str(batch.quantity)))
            self.expired_table.setItem(
                row, 2, QTableWidgetItem(str(batch.expiration_date))
            )
            self.expired_table.setItem(row, 3, QTableWidgetItem(batch.lot_number or ""))
            self.expired_table.setItem(row, 4, QTableWidgetItem(batch.location or ""))

        for batch in self.expiring:
            print(
                "PRODOTTO IN SCADENZA:",
                batch.product.name,
                batch.quantity,
                batch.expiration_date,
            )

            row = self.expiring_table.rowCount()
            self.expiring_table.insertRow(row)

            self.expiring_table.setItem(row, 0, QTableWidgetItem(batch.product.name))
            self.expiring_table.setItem(row, 1, QTableWidgetItem(str(batch.quantity)))
            self.expiring_table.setItem(
                row, 2, QTableWidgetItem(str(batch.expiration_date))
            )
            self.expiring_table.setItem(
                row, 3, QTableWidgetItem(batch.lot_number or "")
            )
            self.expiring_table.setItem(row, 4, QTableWidgetItem(batch.location or ""))
