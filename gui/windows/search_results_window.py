from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.inventory_service import get_product_inventory


class SearchResultsWindow(QWidget):
    def __init__(self, products):
        super().__init__()

        self.products = products

        self.setWindowTitle("Serach Results")
        self.resize(700, 400)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(
            ["Prodotto", "Quantità", "Scadenza", "Lotto", "Posizione"]
        )
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.results_table)

        self.setLayout(layout)

        self.populate_table()

    def populate_table(self):

        for product in self.products:
            batches, _ = get_product_inventory(product)

            for batch in batches:
                row = self.results_table.rowCount()
                self.results_table.insertRow(row)

                self.results_table.setItem(row, 0, QTableWidgetItem(product.name))
                self.results_table.setItem(
                    row, 1, QTableWidgetItem(str(batch.quantity))
                )
                self.results_table.setItem(
                    row, 2, QTableWidgetItem(str(batch.expiration_date))
                )
                self.results_table.setItem(
                    row, 3, QTableWidgetItem(str(batch.lot_number) or "")
                )
                self.results_table.setItem(
                    row, 4, QTableWidgetItem(str(batch.location) or "")
                )
