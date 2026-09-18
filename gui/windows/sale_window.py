from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCompleter,
    QInputDialog,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.movement_service import create_sale
from services.product_service import get_all_products


class SaleWindow(QWidget):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.setWindowTitle("Prelievo")
        self.resize(500, 500)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca prodotto...")

        self.products = get_all_products(self.session)
        products_names = [product.name for product in self.products]
        self.completer = QCompleter(products_names)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_bar.setCompleter(self.completer)

        self.products_table = QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setHorizontalHeaderLabels(
            ["Prodotto", "Scadenza", "Quantità"]
        )
        self.products_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.products_table.cellDoubleClicked.connect(self.select_batch)

        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.products_table)

        self.setLayout(layout)

        self.batch_rows = []

        self.load_products()

    def load_products(self):
        for product in self.products:
            for batch in product.batches:
                row = self.products_table.rowCount()
                self.products_table.insertRow(row)

                self.products_table.setItem(row, 0, QTableWidgetItem(product.name))
                self.products_table.setItem(
                    row, 1, QTableWidgetItem(str(batch.expiration_date or ""))
                )
                self.products_table.setItem(
                    row, 2, QTableWidgetItem(str(batch.quantity))
                )

                self.batch_rows.append(batch)

    def select_batch(self, row):
        batch = self.batch_rows[row]
        quantity, ok = QInputDialog.getInt(
            self,
            "Prelievo",
            f"Quantità da prelevare da {batch.product.name}:",
            1,
            1,
            batch.quantity,
        )
        if not ok:
            return

        movement = create_sale(
            batch=batch,
            quantity=quantity,
            movement_date=date.today(),
        )

        self.session.add(movement)
        self.session.commit()

        self.products_table.setItem(row, 2, QTableWidgetItem(str(batch.quantity)))

        self.close()
