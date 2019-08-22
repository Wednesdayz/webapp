from order import Orders, PiggyBackOrder
from Item import Item, food, meal, drinks
from flask import Flask, render_template, redirect, request, flash, abort, session, jsonify
from jinja2 import StrictUndefined
from model import connect_to_db, db, Customer, Location, Product

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

    pass

@app.route('/login', methods=['POST'])
def process_login():
    """Process login data. Add user_id to session"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(Customer).filter(Customer.email == email).first()

    if user and password == user.password_hash:

        session['email'] = email
        if session.get('email'):
            flash("Login successful!")
            return redirect("/")
        else:
            return "CookieFail"

    else:

        return "Fail"
    

@app.route('/logout')
def process_logout():
    """Log user out, redirect to /products"""

    del session['email']

    flash("You have been logged out.")

    return redirect("/homepage.html")

@app.route('/register')
def show_register():
    """Show registration form"""

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def process_registration():
    """Process user registration"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    country = request.form.get("country")

    user = Customer(first_name=first_name, last_name=last_name, email=email, password_hash=password, phone=phone, country=country)
    
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

@app.route('/products', methods=["POST"])
def add_products_to_cart():
    """Add product to cart from button click"""

    product_id = int(request.form.get("productId"))  # this can be wrapped in a func to DRY up code
    product = Product.query.get(product_id)
    session["cart"] = session.get("cart", {})
    # session["cart_total"] = session.get("cart_total", 0) + product.price
    session["cart"][product_id] = session["cart"].get(product_id, 0) + 1

    cart = session["cart"]
    print(cart)

    return redirect("/products")

@app.route('/products/<int:product_id>')  # takes product_id as an INTEGER
def show_product_page(product_id):
    """Query database for product info and display results"""

    product = Product.query.get(product_id)

    return render_template("product_page.html", product=product)


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