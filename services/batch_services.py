from datetime import date

from database.models import Batch


def create_batch(
    expiration_date: date | None,
    product,
    lot_number=None,
    location=None,
    arrival_date=None,
):
    batch = Batch(
        quantity=0,
        expiration_date=expiration_date,
        product=product,
        lot_number=lot_number,
        location=location,
        arrival_date=arrival_date,
    )

    return batch
