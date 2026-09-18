import os
from datetime import date, datetime

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database.database import Session
from database.models import Batch
from services.batch_services import create_batch
from services.inventory_service import check_expirations
from services.movement_service import (
    create_arrival,
    create_expired,
    create_sale,
    get_all_movements,
)
from services.product_service import (
    create_product,
    get_all_products,
    get_product_by_barcode,
    get_product_by_name,
    get_products_by_category,
    search_products,
)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

ACCESS_CODE_HASH = os.environ["ACCESS_CODE_HASH"]


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        code = request.form["code"]

        if check_password_hash(ACCESS_CODE_HASH, code):

            session["logged_in"] = True

            return redirect(url_for("home"))

        return render_template("login.html", error="Codice non corretto.")

    return render_template("login.html")


@app.before_request
def require_login():

    if request.endpoint in ["login", "static"]:
        return

    if not session.get("logged_in"):
        return redirect(url_for("login"))


@app.route("/")
def home():
    session = Session()

    products = get_all_products(session)

    session.close()

    return render_template("home.html", products=products)


@app.route("/magazzino")
def warehouse():
    session = Session()

    products = get_all_products(session)

    session.close()

    return render_template("warehouse.html", products=products)


@app.route("/magazzino/<category>")
def warehouse_category(category):

    session = Session()

    products = get_products_by_category(session, category)
    all_products = get_all_products(session)

    session.close()

    return render_template(
        "warehouse.html",
        products=products,
        category=category,
        all_products=all_products,
    )


@app.route("/cerca")
def search():
    search_text = request.args.get("q", "").strip()

    session = Session()

    products = search_products(session, search_text)

    session.close()

    return render_template("warehouse.html", products=products)


@app.route("/nuovo-arrivo", methods=["GET", "POST"])
def new_arrival():

    if request.method == "GET":
        return render_template("new_arrival.html")

    session = Session()

    try:
        name = request.form["name"].strip()
        barcode = request.form["barcode"].strip() or None
        category = request.form["category"].strip() or None
        quantity = int(request.form["quantity"])

        expiration_date = request.form["expiration_date"] or None

        lot_number = request.form["lot_number"].strip() or None
        location = request.form["location"].strip() or None

        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, "%d/%m/%Y")

        arrival_date = date.today()

        product = get_product_by_name(session, name)

        if product is None:
            product = create_product(name=name, barcode=barcode, category=category)

            session.add(product)
            session.flush()

        batch = create_batch(
            expiration_date=expiration_date,
            product=product,
            lot_number=lot_number,
            location=location,
            arrival_date=arrival_date,
        )

        session.add(batch)
        session.flush()

        movement = create_arrival(
            batch=batch, quantity=quantity, movement_date=arrival_date
        )

        session.add(movement)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    return render_template("new_arrival.html")


@app.route("/barcode/<barcode>")
def get_product_from_barcode(barcode):

    session = Session()

    try:

        product = get_product_by_barcode(session, barcode)

        if product is None:
            return {"found": False}

        return {"found": True, "name": product.name, "category": product.category}

    finally:
        session.close()


@app.route("/scadenze")
def expired_products():

    session = Session()

    expired, expiring = check_expirations(session, 30)

    session.close()

    return render_template("expired_products.html", expired=expired, expiring=expiring)


@app.route("/elimina_scadenza", methods=["POST"])
def delete_expired():

    session = Session()

    batch_id = int(request.form["batch_id"])

    batch = session.get(Batch, batch_id)

    if batch is None:
        raise ValueError("Batch non trovato.")

    movement = create_expired(
        batch=batch, quantity=batch.quantity, movement_date=date.today()
    )

    session.add(movement)

    session.commit()

    session.close()

    return redirect(url_for("expired_products"))


@app.route("/prelievo")
def withdrawal():

    session = Session()

    products = get_all_products(session)

    session.close()

    return render_template("withdrawal.html", products=products)


@app.route("/preleva", methods=["POST"])
def create_withdrawal():

    session = Session()

    batch_id = int(request.form["batch_id"])
    quantity = int(request.form["quantity"])

    batch = session.get(Batch, batch_id)

    if batch is None:
        raise ValueError("Batch non trovato.")

    movement = create_sale(batch=batch, quantity=quantity, movement_date=date.today())

    session.add(movement)
    session.commit()

    session.close()

    return redirect(url_for("withdrawal"))


@app.route("/storico")
def movement_history():

    session = Session()

    movements = get_all_movements(session)

    session.close()

    return render_template("movement_history.html", movements=movements)


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
