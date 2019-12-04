import requests
from os import environ
from flask import session, request
import stripe
from model import (connect_to_db, db, Product, Tag, Product_Tag, Customer, Pickup, Delivery, Order, Icon, Delivery_Quantity,
                   Order_Quantity)
import arrow


def split_params(param_list):

    params = []
    for param in param_list:
        param = param.split()
        for adj in ['Organic', 'Fresh', '(Frozen)', 'Pre-Washed']:
            if adj in param:
                param.remove(adj)
        params.append(param)
    return params

def pay_for_cart():
    """Utilize stripe API"""

    placed_at = arrow.utcnow()
    print ("placed at ", placed_at)
    customer = db.session.query(Customer).filter(Customer.email == session['email']).one()
    print ("customer", customer)
    order = Order(customer_id=customer.user_id, placed_at=placed_at, total=session["cart_total"], pickup_id=1)  # change pickup!!!

    print ("order = ", order)
    db.session.add(order)
    print ("added order")
    db.session.commit()
    print ("committed order")

    order_id = db.session.query(Order.order_id).filter(Order.customer_id == customer.user_id,
                                                       Order.placed_at == placed_at).one()
    print (order_id, " is the order_id!!!!!!!!!!!!")

    token = request.form.get('stripeToken')

    print ("token is ", token)

    stripe.api_key = environ["STRIPE_TEST_SECRET"]

    try:
        stripe.Charge.create(amount=int(session["cart_total"] * 100),
                             currency="usd",
                             source=token,  # obtained with Stripe.js
                             metadata={'order_id': order_id[0],
                                       'customer_id': customer.user_id},
                             statement_descriptor="Farm to Front Door CSA",
                             description="Farm to Front Door CSA"
                             )
        del session['cart']
        del session['cart_total']
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err = body['error']

        print ("Status is: %s" % e.http_status)
        print ("Type is: %s" % err['type'])
        print ("Code is: %s" % err['code'])
        # param is '' in this case
        print ("Param is: %s" % err['param'])
        print ("Message is: %s" % err['message'])
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        pass