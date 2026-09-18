from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.product_service import get_all_products


class AllProductsWindow(QWidget):
    def __init__(self, session):
        super().__init__()

        self.setWindowTitle("Giacenze")
        self.resize(800, 500)

        self.session = session

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(
            ["Prodotto", "Quantità", "Scadenza", "Lotto", "Posizione"]
        )
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.items_table)

        self.setLayout(layout)

        self.batch_rows = []

        self.populate_table()

    def populate_table(self):
        products = get_all_products(self.session)

        for product in products:
            for batch in product.batches:
                row = self.items_table.rowCount()
                self.items_table.insertRow(row)

                self.items_table.setItem(row, 0, QTableWidgetItem(product.name))
                self.items_table.setItem(row, 1, QTableWidgetItem(str(batch.quantity)))
                self.items_table.setItem(
                    row, 2, QTableWidgetItem(str(batch.expiration_date or ""))
                )
                self.items_table.setItem(
                    row, 3, QTableWidgetItem(batch.lot_number or "")
                )
                self.items_table.setItem(row, 4, QTableWidgetItem(batch.location or ""))

                self.batch_rows.append(batch)
