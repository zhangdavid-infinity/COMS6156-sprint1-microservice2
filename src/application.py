from flask import Flask, Response, request,redirect, url_for
from datetime import datetime
import json
from shop_resource import ShopResource
from order_resource import OrderResource
from product_resource import ProductResource
from flask_cors import CORS
from sns import NotificationMiddlewareHandler
from flask_dance.contrib.google import make_google_blueprint, google
from secure import check_path
import os

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)
'''
client_id = "884647360293-b86d0287p2hftqe8r9fbn0a92e8mjsta.apps.googleusercontent.com"
client_secret = "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"
app.secret_key = "supersekrit"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
blueprint = make_google_blueprint(
     client_id=client_id,
     client_secret=client_secret,
     reprompt_consent=True,
     scope=["profile", "email"]
 )
app.register_blueprint(blueprint, url_prefix="/login")
google_blueprint = app.blueprints.get("google")

@app.before_request
def before_request():
     print("checking before request")
     #print(google.get(info))
     #result_pass = check_path(request, google, google_blueprint)
     print(url_for('google.login'))
     if not google.authorized:
         return redirect(url_for('google.login'))
'''
@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "COMS6156-sprint1-microservice2",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/shop/<shopID>", methods=["GET","DELETE","PUT"])
def change_shop_by_shopID(shopID):

    if request.method == 'GET':

        result = ShopResource.get_by_key(shopID)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp
    elif request.method == 'DELETE':

        result = ShopResource.delete_by_key(shopID)
        if result:
            rsp = Response(json.dumps({'status':200}), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        print(rsp)
        return rsp


@app.route("/api/shop/", methods=["POST",'PUT'])
def update_shop():
    if request.method == 'POST':
        shop = request.get_json()
        result = ShopResource.add(shop)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
            sns = NotificationMiddlewareHandler.get_sns_client()
            print("Got SNS Client!")
            tps = NotificationMiddlewareHandler.get_sns_topics()
            print("SNS Topics = \n", json.dumps(tps, indent=2))

            message = {"test": "new shop created"}
            NotificationMiddlewareHandler.send_sns_message(
                "arn:aws:sns:us-east-1:606830512180:6156-shop",
                message
            )

        else:
            rsp = Response("Internal server error!", status=500, content_type="text/plain")


        return rsp

    elif request.method == 'PUT':
        shop = request.get_json()
        result = ShopResource.update(shop)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("Internal server error", status=500, content_type="text/plain")

        return rsp



@app.route("/api/product/<productID>", methods=["GET", "DELETE"])
def get_product_by_productID(productID):
    if request.method == 'GET':

        result = ProductResource.get_by_key(productID)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp
    elif request.method == 'DELETE':

        result = ProductResource.delete_by_key(productID)

        if result:
            rsp = Response(json.dumps({'status': 200}), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp

@app.route("/api/product/", methods=["POST",'PUT'])
def update_product():
    if request.method == 'POST':
        product = request.get_json()
        result = ProductResource.add(product)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("Internal server error", status=500, content_type="text/plain")

        return rsp

    elif request.method == 'PUT':
        product = request.get_json()
        result = ProductResource.update(product)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("Internal server error", status=500, content_type="text/plain")

        return rsp
@app.route("/api/order/<orderID>", methods=["GET", "DELETE"])
def get_order_by_orderID(orderID):
    if request.method == 'GET':

        result = OrderResource.get_by_key(orderID)

        if result:
            rsp = Response(json.dumps(result, default=str), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp
    elif request.method == 'DELETE':
        result = OrderResource.delete_by_key(orderID)

        if result:
            rsp = Response(json.dumps({'status': 200}), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp

@app.route("/api/order/", methods=["POST",'PUT'])
def update_order():
    if request.method == 'POST':
        order = request.get_json()
        result = OrderResource.add(order)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("Internal server error", status=500, content_type="text/plain")

        return rsp

    elif request.method == 'PUT':
        order = request.get_json()
        result = OrderResource.update(order)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("Internal server error", status=500, content_type="text/plain")

        return rsp

@app.route("/api/order/count/customerid", methods=["GET"])
def get_count():
    result = OrderResource.get_count_by_key(customerid)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Internal server error", status=500, content_type="text/plain")

    return rsp



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

