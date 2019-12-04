from order import Orders, PiggyBackOrder
from Item import Item, food, meal, drinks
from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify
from jinja2 import StrictUndefined
from model import *
import api
from math import floor
import functions
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'Bbklct321'


#For debugging - see Jinja fails
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


#homepage
@app.route('/')
def homepage():
    """Display Homepage"""
    
    return render_template("homepage.html")

@app.route('/login')  # currently using modal window instead of route...
def show_login():
    """Show login form"""

    return render_template("homepage.html")

@app.route('/login', methods=['POST'])
def process_login():
    """Process login data. Add user_id to session"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(Customer).filter(Customer.email == email).first()

    if user and pbkdf2_sha256.verify(password, user.password_hash):

        session['email'] = email
        if session.get('email'):
            flash("Login successful!")
            return "Success"
        else:
            return "CookieFail"

    else:

        return "Fail"
    

@app.route('/logout')
def process_logout():
    """Log user out, redirect to /products"""

    del session['email']

    flash("You have been logged out.")

    return redirect("/")

@app.route('/register')
def show_register():
    """Show registration form"""

    return render_template("register.html")

@app.route('/forgot_password')
def show_forgot_password():
    """Show forgot password form"""

    return render_template("forgot_password.html")

@app.route('/forgot_password', methods=['POST'])
def process_forgot_password():
    email = request.form.get("email")
    phone = request.form.get("phone")
    country = request.form.get("country")

    user = db.session.query(Customer).filter(Customer.email == email).first()

    if not user:
        flash("email does not exist in our database")
    elif user.phone == phone and user.country == country:
        print(user)
        return render_template("reset_password.html", customer=user)
    elif(user.phone is not phone):
        flash("Phone number given does not match email given")
    elif(user.country is not country):
        flash("Country does not match database credentials")
    
    print("hello")
    
    #passing by json

    return render_template("forgot_password.html")

@app.route('/reset_password')
def show_reset_password():
    """show rest password form"""
    
    return redirect("reset_password.html")

@app.route('/reset_password', methods=['GET','POST'])
def process_reset_password():
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    print(customer)
    if password is confirm_password:
        password = pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)
        customer.password_hash = password
        flash("account password has been reset, please login again")
        return render_template("homepage.html")
    else:
        flash("passwords did not match, please try again")
        return render_template("reset_password.html", customer=customer)


@app.route('/register', methods=['POST'])
def process_registration():
    """Process user registration"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    password = pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)
    phone = request.form.get("phone")
    street_address = request.form.get("street_address")
    zipcode = request.form.get("zipcode")
    state = request.form.get("state")
    country = request.form.get("country")

    user = Customer(first_name=first_name, last_name=last_name, email=email, password_hash=password, phone=phone,street_address=street_address, zipcode=zipcode, state=state, country=country)
    
    db.session.add(user)
    db.session.commit()

    session['email'] = email
    if session.get('email'):
        flash("Registration successful! Welcome to Beyond")
    else:
        flash("Please enable cookies to log in")

    return redirect("/products.html")

@app.route('/account')
def show_account():
    """Show user's info, past orders"""

    customer = db.session.query(Customer).filter(Customer.email == session['email']).one()  

    return render_template("account.html", customer=customer)

@app.route('/products')
def filter_products():
    """Allow customers to filter products"""

    return render_template("filter.html")

@app.route('/search')
def show_search_results():
    """Query database for search results"""

    terms = request.args.get("terms").title()

    categories = db.session.query(Product.category).group_by(Product.category).all()
    products = db.session.query(Product).filter(Product.name.like('%' + terms + '%')).all()

    return render_template("products.html", products=products, categories=categories)



@app.route('/filters.json')
def serve_filtered_products_json():
    """Query database for product list & display results"""

    filters = request.args.getlist("filters")
    if filters:
        prods = db.session.query(Product).filter(Product.category.in_(filters)).order_by(Product.category).all()
    else:
        prods = db.session.query(Product).all()

    categories = db.session.query(Product.category).group_by(Product.category).all()
    products = {}
    for prod in prods:
        products[prod.product_id] = {"name": prod.name, "id": prod.product_id, "price": prod.price, "img": prod.img, "weight": prod.weight, "unit": prod.unit}
        # if prod.icon_id:
        #     products[prod.product_id]["icon"] = prod.icon.url

    return jsonify(**{"products": products, "categories": categories})

@app.route('/products', methods=["POST"])
def add_products_to_cart():
    """Add product to cart from button click"""

    product_id = request.form.get("productId")  # this can be wrapped in a func to DRY up code
    product = Product.query.get(int(product_id))
    session["cart"] = session.get("cart", {})
    # session["cart_total"] = session.get("cart_total", 0) + product.price
    session["cart"][product_id] = int(session["cart"].get(product_id, 0)) + 1

    cart = session["cart"]
    print(cart)                 

    return redirect("/products")


@app.route('/products/<int:product_id>')  # takes product_id as an INTEGER
def show_product_page(product_id):
    """Query database for product info and display results"""

    product = Product.query.get(product_id)

    return render_template("product_page.html", product=product)


@app.route('/products/<int:product_id>', methods=["POST"])  # takes product_id as an INTEGER
def add_product_to_cart(product_id):
    """Add product to cart from button click on prod page"""

    product_id = request.form.get("productId")

    session["cart"] = session.get("cart", {})
    # session["cart_total"] = session.get("cart_total", 0) + product.price
    session["cart"][product_id] = int(session["cart"].get(product_id, 0)) + 1

    cart = session["cart"]
    print(cart)

    return redirect('/products/' + str(product_id))

@app.route('/locations')
def show_locations():
    """Show local pickup locations"""

    pickups = db.session.query(Pickup).filter(Pickup.pickup_id > 1).all()

    return render_template("locations.html", pickups=pickups)

@app.route('/cart')
def show_cart():
    """Query session for cart contents and display results"""

    return render_template("cart.html")

@app.route('/add-item', methods=['POST'])
def add_to_cart_from_ng():
    """Update cart from Angular AJAX Post"""

    session['cart'] = session.get('cart', {})
    product_id = request.json.get('product_id')
    session['cart'][str(product_id)] = session['cart'].get(str(product_id), 0) + 1
    session.modified = True

    if product_id:
        return "Success!" 
    return "Missing product id"


@app.route('/update-cart', methods=['POST'])
def update_cart_from_ng():
    """Update cart from dropdowns on cart page"""

    print(session['cart'])
    product_id = int(request.json.get('product_id'))
    qty = int(request.json.get('qty'))
    print(product_id)
    print(qty)

    if product_id and qty:
        session['cart'][str(product_id)] = qty
        session.modified = True
        print(session['cart'])
        return "Success"
    else:
        return "Missing parameters"

@app.route('/cart', methods=['POST'])
def update_cart():
    """Process delivery options"""

    delivery_type = request.json.get("delivery")
    big_address = request.json.get("address")
    street_address = big_address["street"]
    zipcode = big_address["zipcode"]
    print(delivery_type, " is the delivery_type")
    print(street_address, " is the street_address")
    print(zipcode, " is the zipcode")

    if delivery_type and street_address and zipcode:
        session['delivery'] = {'delivery': delivery_type, 'address': street_address, 'zipcode': zipcode}
        print(session['delivery'])
        print(session['cart'])
        return "Success"
    else:
        return "Fail"


@app.route('/delete-product', methods=['POST'])
def delete_from_cart():
    """Delete item from cart"""
    product_id = request.json.get('product_id')


    if product_id:
        del session['cart'][str(product_id)]
        session.modified = True
        return "Success"
    else:
        return "Missing product_id"


@app.route('/cart.json')
def get_cart_json():
    """Gets product info from database and returns in json"""
    
    result_objects = db.session.query(Product).filter(Product.product_id.in_(session["cart"].keys())).all()
    result = {"contents": [], "cart": {}}
    print(result)

    for product_obj in result_objects:
        print(session["cart"])
        result["cart"][product_obj.product_id] = {"name": product_obj.name,
                                                  "qty": session["cart"][str(product_obj.product_id)],
                                                  "description": product_obj.description,
                                                  "weight": product_obj.weight,
                                                  "unit": product_obj.unit,
                                                  "price": product_obj.price,
                                                  "price_per": product_obj.price_per,
                                                  "per_unit": product_obj.per_unit,
                                                  "product_id": product_obj.product_id,
                                                  "icon": None}
        print(result)
        if product_obj.icon_id:
            result["cart"][product_obj.product_id]["icon"] = product_obj.icon.url
        result["contents"].append(str(product_obj.product_id))

    return jsonify(**result)

@app.route('/customer.json')
def get_customer_json():
    """Get customer info from database and return in json"""

    #throws an error if customer not logged in!

    if 'email' in session:

        customer = db.session.query(Customer).filter(Customer.email == session['email']).first()

        return jsonify(customer_id=customer.user_id, email=customer.email,
                       street_address=customer.street_address, zipcode=customer.zipcode,
                       state=customer.state)
    else:

        return jsonify(customer_id=None, email=None,
                       street_address=None, zipcode=None,
                       state=None)


@app.route('/pickups.json')
def get_pickups_json():
    """Provide JSON for pickup locations"""

    pickup_json = {"locations": {}, "ids": []}
    pickups = Pickup.query.filter(Pickup.pickup_id > 1).all()

    for pickup in pickups:
        pickup_json["locations"][pickup.name] = {"id": pickup.pickup_id,
                                                 "name": pickup.name,
                                                 "description": pickup.description,
                                                 "address": pickup.street_address,
                                                 "zipcode": pickup.zipcode}
        pickup_json["ids"].append(pickup.name)

    return jsonify(**pickup_json)

@app.route('/checkout')
def check_out():
    """Check out"""

    cart = Product.query.filter(Product.product_id.in_(session['cart'].keys())).all()
    functions.get_cart_total(cart)

    return render_template("checkout.html", cart=cart)

@app.route('/checkout', methods=['POST'])
def process_payment():
    """Process payment"""

    cart = Product.query.filter(Product.product_id.in_(session['cart'].keys())).all()
    functions.get_cart_total(cart)

    api.pay_for_cart()

    return render_template("success.html")



@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""

    return render_template('404.html'), 404

if __name__ == "__main__":
    # Change app.debug to False before launch
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")