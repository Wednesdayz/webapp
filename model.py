from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import create_engine 
import arrow


db = SQLAlchemy()

class Customer(db.Model):
    """Customer of FACT food"""
    
    __tablename__ = "customers"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(500), nullable=False)
    orders = db.relationship("Order", backref="customer")

    def __init__(self, first_name,last_name,email,password_hash,phone,country):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.country = country

class Location(db.Model):
    """Pickup locations"""

    __tablename__ = "locations"

    vendor = db.Column(db.String(500), nullable=True)
    vendor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    street_address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Unicode, nullable=True)
    zipcode = db.Column(db.String(15), nullable=False)
    suburb = db.Column(db.String(100), nullable=False, default="Sydney")
    state = db.Column(db.String(100), nullable=False, default="New South Wales")

    def __init__(self, vendor, vendor_id, street_address, description, zipcode, suburb, state):
        self.vendor = vendor
        self.vendor_id = vendor_id
        self.street_address = street_address
        self.description = description
        self.zipcode = zipcode
        self.suburb = suburb
        self.state = state

class Product(db.Model):
    """Product sold by Farm to Front Door"""

    __tablename__ = "products"

    name = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.Unicode, nullable=True)  # db.Text(collation='utf8', convert_unicode=True)
    units = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Numeric(asdecimal=False), nullable=False)  # db.Numeric(asdecimal=False)
    category = db.Column(db.String(50), nullable=True)
    img = db.Column(db.String(500), nullable=True)
    icon_id = db.Column(db.Integer, db.ForeignKey('icons.icon_id'), nullable=True)
    color = db.Column(db.String(10), nullable=True)
    search_term = db.Column(db.String(50), nullable=True)
    search_strength = db.Column(db.Integer, nullable=True)

    icon = db.relationship("Icon", backref="products")

    def __init__(self, name, product_id, description, units, price, category, img, icon_id, color, search_term, search_strength, icon):
        self.name = name
        self.product_id = product_id
        self.description = description
        self.units = units
        self.price = price 
        self.category = category 
        self.img = img
        self.icon_id = icon_id
        self.color = color
        self.search_term = search_term
        self.search_strength = search_strength
        self.icon = icon


class Icon(db.Model):
    """Icon for web usage"""

    __tablename__ = "icons"

    icon_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    credit = db.Column(db.String(100), nullable=False)

    def __init__(self, icon_id, url, credit):
        self.icon_id = icon_id
        self.url = url
        self.credit = credit

class Order(db.Model):
    """An order placed by a customer, composed of Order-Quantities"""

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.user_id"), nullable=False)
    placed_at = db.Column(ArrowType, nullable=False)  # or db.DateTime v. db.TimeStamp?
    total = db.Column(db.Numeric, nullable=False)
    pickup_id = db.Column(db.Integer, db.ForeignKey("locations.vendor_id"), nullable=False)
    received_at = db.Column(ArrowType, nullable=True)  # or db.DateTime v. db.TimeStamp?
    pickup_location = db.relationship("Location", backref="locations")
    quantities = db.relationship("Order_Quantity", backref="order")

    def __init__(self, order_id, customer_id, placed_at, total, received_at, pickup_id, pickup_location, quantities):
        self.order_id = order_id
        self.customer_id = customer_id
        self.placed_at = placed_at
        self.total = total
        self.pickup_id = pickup_id
        self.received_at = received_at
        self.pickup_id = pickup_id
        self.pickup_location = pickup_location
        self.quantities = quantities

class Order_Quantity(db.Model):
    """An amount of a certain product, in each order"""

    __tablename__ = "order_quantities"

    order_qty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    product_qty = db.Column(db.Integer, nullable=False, default=1)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)

    def __init__(self, order_qty_id, product_id, product_qty, order_id):
        self.order_qty_id = order_qty_id
        self.product_id = product_id
        self.product_qty = product_qty
        self.order_id = order_id

def connect_to_db(app, database='postgresql://postgres:Bbklct321@localhost:5432/Beyond'):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from routes import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")