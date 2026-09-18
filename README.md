# Warehouse Management System

A warehouse management system developed to simplify inventory management for a supermarket warehouse.

The application allows users to manage products, batches, stock movements and expiration dates through a simple web interface.

The project was initially developed as a desktop application using **PySide6** and was later redesigned as a **Flask web application**.

⚠️ Note: This project is currently under development and is not a final version. Features, structure and functionality are subject to continuous changes and improvements.
---

## Features

* 🔐 Login with password-protected access
* 📦 Product and batch management
* 📥 Registration of incoming goods
* 📤 Product withdrawals
* 📊 Current stock monitoring
* 🔎 Product search by name, barcode or category
* 🏷️ Product categorization
* 📅 Expiration date monitoring
* ⚠️ Detection of expired and soon-to-expire products
* 📋 Movement history
* 📷 Barcode scanning through the device camera
* 🗄️ PostgreSQL database

---

## Technologies

### Backend

* Python
* Flask
* SQLAlchemy
* PostgreSQL

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2

### Other

* PySide6 *(previous desktop interface)*
* `html5-qrcode` for barcode scanning
* `python-dotenv` for environment variables

---

## Project Structure

```text
warehouse_management_system/
│
├── database/
│   ├── database.py
│   └── models.py
│
├── enums/
│   └── movement_type.py
│
├── services/
│   ├── product_service.py
│   ├── batch_services.py
│   ├── inventory_service.py
│   └── movement_service.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── warehouse.html
│   ├── warehouse_category.html
│   ├── new_arrival.html
│   ├── withdrawal.html
│   ├── expired_products.html
│   └── movement_history.html
│
├── static/
│   └── style.css
│
├── app.py
├── main.py
├── create_tables.py
├── migrate_data.py
├── requirements.txt
├── .env
└── .gitignore
```

---

## Application Architecture

The application is divided into different layers:

```text
Web Interface
     ↓
   Flask
     ↓
  Services
     ↓
   Models
     ↓
 PostgreSQL
```

The service layer contains the main business logic, while Flask handles the web interface and routing.

---

## Database

The application uses **PostgreSQL** to store:

* Products
* Batches
* Current stock quantities
* Expiration dates
* Lot numbers
* Warehouse locations
* Stock movements

Each stock movement is associated with a specific batch.

The current quantity of a batch represents the amount of stock still available, while movements keep track of how that quantity has changed over time.

---

## Stock Movements

The system currently supports four types of movements:

* `ARRIVAL` – incoming goods
* `SALE` – product withdrawal
* `EXPIRED` – expired products removed from stock
* `ADJUSTMENT` – manual stock correction (still a work in progress)

This allows the current stock to be monitored while maintaining a history of inventory changes.

---

## Running the Application

Clone the repository:

```bash
git clone <repository-url>
cd warehouse_management_system
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a PostgreSQL database named:

```text
warehouse
```

Configure the required environment variables in `.env`:

```env
SECRET_KEY=your-secret-key
ACCESS_CODE_HASH=your-password-hash
DATABASE_URL=your-database-url
```

Create the database tables if necessary:

```bash
python create_tables.py
```

Start the web application:

```bash
python app.py
```

The application can then be accessed from the browser.

---

## Desktop Application

The project also contains the original PySide6 desktop interface.

The desktop application can be started through:

```bash
python main.py
```

This interface was the initial version of the project and is kept separately from the Flask web application.

---

## Current Status

The project is currently being developed as a **local web application**, intended to run on the computer used in the supermarket warehouse.

The current setup is designed to keep the application and PostgreSQL database locally on the warehouse computer, without requiring an external server.

Future improvements may include:

* Easier application startup
* Automated database backups
* Improved barcode management
* Multi-device access
* Online deployment
* Additional inventory management features

---

## Purpose

This project was created as a practical software engineering project to develop a real-world solution for warehouse inventory management.

The main goal is to replace manual stock tracking with a simple digital system that makes it easier to monitor inventory, batches, expiration dates and stock movements.
