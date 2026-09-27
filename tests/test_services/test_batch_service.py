from database.models import Product
from services.batch_services import create_batch


def test_create_batch():
    expiration_date = 12 / 10 / 2027
    product = Product(name="Latte")

    batch = create_batch(expiration_date=expiration_date, product=product)

    assert batch.expiration_date == expiration_date
    assert batch.product == product
