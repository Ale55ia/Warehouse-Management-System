from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCompleter,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.windows.all_products_window import AllProductsWindow
from gui.windows.expiring_products_window import ExpiringProductsWindow
from gui.windows.movements_history_window import MovementsHistoryWindow
from gui.windows.new_product_window import NewProductWindow
from gui.windows.sale_window import SaleWindow
from gui.windows.search_results_window import SearchResultsWindow
from services.inventory_service import check_expirations
from services.movement_service import get_all_movements
from services.product_service import get_all_products, search_products


class HomeWindow(QWidget):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.setWindowTitle("Warehouse Management System")
        self.resize(600, 400)

        title = QLabel("Warehouse Management System")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca prodotti...")

        self.search_button = QPushButton("Cerca")
        self.search_button.clicked.connect(self.search_product)

        products = get_all_products(self.session)
        products_names = [product.name for product in products]
        self.completer = QCompleter(products_names)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_bar.setCompleter(self.completer)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        self.new_product_button = QPushButton("Nuovo Prodotto")
        self.new_product_button.clicked.connect(self.open_new_product_window)

        self.expiring_button = QPushButton("Prodotti in Scadenza")
        self.expiring_button.clicked.connect(self.show_expiring_products)

        self.movements_button = QPushButton("Storico dei Movimenti")
        self.movements_button.clicked.connect(self.show_movements_hisotry)

        self.sale_button = QPushButton("Prelievo")
        self.sale_button.clicked.connect(self.show_sale)

        self.all_products_button = QPushButton("Magazzino")
        self.all_products_button.clicked.connect(self.show_all_products)

        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addLayout(search_layout)
        layout.addWidget(self.all_products_button)
        layout.addWidget(self.new_product_button)
        layout.addWidget(self.sale_button)
        layout.addWidget(self.expiring_button)
        layout.addWidget(self.movements_button)

        self.setLayout(layout)

    def search_product(self):
        search_text = self.search_bar.text()

        products = search_products(self.session, search_text)

        if not products:
            QMessageBox.information(
                self, "Prodotto non trovato", "Non è stato trovato nessun prodotto."
            )
            return

        self.search_results_window = SearchResultsWindow(products)
        self.search_results_window.show()

    def open_new_product_window(self):
        self.new_product_window = NewProductWindow(self.session)
        self.new_product_window.show()

    def show_expiring_products(self):
        expired, expiring = check_expirations(self.session, days=30)
        self.expiring_products_window = ExpiringProductsWindow(expired, expiring)
        self.expiring_products_window.show()

    def show_movements_hisotry(self):
        movements = get_all_movements(self.session)
        self.movements_hostory_window = MovementsHistoryWindow(movements)
        self.movements_hostory_window.show()

    def show_sale(self):
        self.sale_window = SaleWindow(self.session)
        self.sale_window.show()

    def show_all_products(self):
        self.all_products_window = AllProductsWindow(self.session)
        self.all_products_window.show()
