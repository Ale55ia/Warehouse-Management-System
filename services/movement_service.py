from sqlalchemy import desc, select
from sqlalchemy.orm import joinedload

from database.models import Batch, Movement
from enums.movement_type import MovementType


def _create_movement(batch, quantity, movement_type, movement_date):
    if batch.quantity + quantity < 0:
        raise ValueError(
            f"Operazione non valida: il batch contiene solo {batch.quantity} pezzi."
        )

    batch.quantity += quantity

    movement = Movement(
        batch=batch,
        quantity=quantity,
        movement_type=movement_type,
        movement_date=movement_date,
    )

    return movement


def create_arrival(batch, quantity, movement_date):
    if quantity <= 0:
        raise ValueError("La quantità deve essere maggiore di zero.")

    return _create_movement(
        batch=batch,
        quantity=quantity,
        movement_type=MovementType.ARRIVAL,
        movement_date=movement_date,
    )


def create_sale(batch, quantity, movement_date):
    if quantity <= 0:
        raise ValueError("La quantità deve essere maggiore di zero.")

    return _create_movement(
        batch=batch,
        quantity=-quantity,
        movement_type=MovementType.SALE,
        movement_date=movement_date,
    )


def create_expired(batch, quantity, movement_date):
    if quantity <= 0:
        raise ValueError("La quantità deve essere maggiore di zero.")

    return _create_movement(
        batch=batch,
        quantity=-quantity,
        movement_type=MovementType.EXPIRED,
        movement_date=movement_date,
    )


def create_adjustment(batch, quantity, movement_date):
    if quantity == 0:
        raise ValueError("La rettifica non può essere pari a zero.")

    return _create_movement(
        batch=batch,
        quantity=quantity,
        movement_type=MovementType.ADJUSTMENT,
        movement_date=movement_date,
    )


def get_all_movements(session):
    result = session.execute(
        select(Movement)
        .options(joinedload(Movement.batch).joinedload(Batch.product))
        .order_by(desc(Movement.movement_date))
    )

    return result.scalars().all()
