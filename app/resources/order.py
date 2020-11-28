import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, marshal
from random import getrandbits

from app.extensions import db
from app.models import Product, Order, Item
from app.schemas import order_fields


class Create(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument(
            "product_id", type=int, required=True, help="product_id obrigatorio"
        )
        parser.add_argument("quantity", type=int, required=True, help="quantity")
        args = parser.parse_args()

        product = Product.query.get(args.product_id)

        if not product:
            return {"error": "nao possuimos esse produto"}, 400

        if args.quantity > product.quantity:
            return {"error": "nao possuimos essa quantidade"}, 400

        try:
            order = Order()
            order.reference_id = f"FLS-{getrandbits(16)}"
            db.session.add(order)
            db.session.commit()

            item = Item()
            item.order_id = order.id
            item.product_id = product.id
            item.user_id = current_user["id"]
            item.quantity = args.quantity
            item.price = product.price * args.quantity
            db.session.add(item)
            db.session.commit()
            return marshal(order, order_fields, "order")
        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"error": " nao foi possivel criar seu pedido"}, 500


class Pay(Resource):
    pass


class Notification(Resource):
    pass
