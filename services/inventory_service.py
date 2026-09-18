from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.models import Batch


def get_all_batches(session):
    result = session.execute(select(Batch))

    return result.scalars().all()


def check_expirations(session, days):
    today = date.today()
    limit_date = today + timedelta(days=days)

    expired = (
        session.execute(
            select(Batch)
            .options(joinedload(Batch.product))
            .where(Batch.expiration_date < today)
        )
        .scalars()
        .all()
    )
    expiring = (
        session.execute(
            select(Batch)
            .options(joinedload(Batch.product))
            .where(Batch.expiration_date <= limit_date)
            .where(Batch.expiration_date >= today)
        )
        .scalars()
        .all()
    )

    return expired, expiring


def get_product_inventory(product):
    batches = sorted(product.batches, key=lambda batch: batch.expiration_date)

    total_quantity = sum(batch.quantity for batch in batches)

    return batches, total_quantity
