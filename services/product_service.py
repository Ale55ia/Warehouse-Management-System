from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload

from database.models import Product


def get_product_by_name(session, name):
    result = session.execute(select(Product).where(Product.name == name))

    return result.scalar_one_or_none()


def get_products_by_category(session, category):
    result = session.execute(
        select(Product)
        .where(Product.category == category)
        .options(selectinload(Product.batches))
    )

    products = result.scalars().all()

    products.sort(
        key=lambda product: sum(batch.quantity for batch in product.batches) == 0
    )

    return products


def get_product_by_barcode(session, barcode):
    result = session.execute(select(Product).where(Product.barcode == barcode))

    return result.scalar_one_or_none()


def create_product(name, barcode, category):
    product = Product(name=name, barcode=barcode, category=category)

    return product


def search_products(session, search_text):
    result = session.execute(
        select(Product).where(
            or_(
                Product.name.ilike(f"%{search_text}%"),
                Product.barcode.ilike(f"%{search_text}%"),
                Product.category.ilike(f"%{search_text}%"),
            )
        )
    )

    products = result.scalars().all()

    return products


def get_all_products(session):
    result = session.execute(select(Product).options(selectinload(Product.batches)))

    products = result.scalars().all()

    products.sort(
        key=lambda product: sum(batch.quantity for batch in product.batches) == 0
    )

    return products
