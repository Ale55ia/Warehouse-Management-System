from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from services.batch_services import create_batch
from services.movement_service import create_arrival
from services.product_service import create_product, get_product_by_name


class NewProductWindow(QWidget):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.setWindowTitle("Nuovo Prodotto")
        self.resize(500, 500)

        self.name_label = QLabel("Nome prodotto")
        self.name_input = QLineEdit()

        self.barcode_label = QLabel("Barcode")
        self.barcode_input = QLineEdit()

        self.category_label = QLabel("Categoria")
        self.category_input = QComboBox()
        self.category_input.addItems(
            [
                "Dolci",
                "Bevande",
                "Latticini",
                "Freschi",
                "Pasta",
                "Surgelati",
                "Igiene",
                "Altro",
            ]
        )

        self.quantity_label = QLabel("Quantità")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)

        self.expiration_date_label = QLabel("Scadenza")
        self.expiration_date_input = QDateEdit()
        self.expiration_date_input.setSpecialValueText("")
        self.expiration_date_input.setDate(QDate())

        self.arrival_date_label = QLabel("Data di arrivo")
        self.arrival_date_input = QDateEdit()
        self.arrival_date_input.setDate(QDate.currentDate())

        self.position_label = QLabel("Posizione")
        self.position_input = QLineEdit()

        self.lot_number_label = QLabel("N. lotto")
        self.lot_number_input = QLineEdit()

        self.add_button = QPushButton("Aggiungi prodotto")
        self.add_button.clicked.connect(self.add_product)

        layout = QVBoxLayout()

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(self.barcode_label)
        layout.addWidget(self.barcode_input)

        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)

        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        layout.addWidget(self.expiration_date_label)
        layout.addWidget(self.expiration_date_input)

        layout.addWidget(self.position_label)
        layout.addWidget(self.position_input)

        layout.addWidget(self.lot_number_label)
        layout.addWidget(self.lot_number_input)

        layout.addWidget(self.arrival_date_label)
        layout.addWidget(self.arrival_date_input)

        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_product(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self, "Campo obbligatorio", "Inserisci il nome del prodotto."
            )
            return

        barcode = self.barcode_input.text()
        category = self.category_input.currentText()

        existing_product = get_product_by_name(self.session, name)
        if existing_product is None:
            product = create_product(name=name, barcode=barcode, category=category)
            self.session.add(product)
        else:
            product = existing_product

        quantity = self.quantity_input.value()
        position = self.position_input.text()
        lot_number = self.lot_number_input.text()
        expiration_qdate = self.expiration_date_input.date()
        if expiration_qdate.isValid():
            expiration_date = expiration_qdate.toPython()
        else:
            expiration_date = None
        arrival_date = self.arrival_date_input.date().toPython()

        batch = create_batch(
            expiration_date=expiration_date,
            product=product,
            lot_number=lot_number,
            location=position,
            arrival_date=arrival_date,
        )
        self.session.add(batch)

        movement = create_arrival(
            batch=batch, quantity=quantity, movement_date=arrival_date
        )
        self.session.add(movement)

        self.session.commit()

        self.close()
