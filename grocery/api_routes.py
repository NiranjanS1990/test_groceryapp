from datetime import datetime
from flask_restx import Resource, Namespace
from grocery.api_models import Category_model,Item_model,Category_input_model,Item_input_model
from grocery import db
from grocery.models import Category,Item



ns = Namespace("api",description='Curd opertions')

@ns.route("/Category")
class CategoryListAPI(Resource):
    @ns.marshal_list_with(Category_model)
    def get(self):
     return Category.query.all()
    @ns.expect(Category_input_model)
    @ns.marshal_with(Category_model)
    def post(self):
        category = Category(name=ns.payload["name"],description=ns.payload["description"])
        db.session.add(category)
        db.session.commit()
        return category, 201

@ns.route("/Category/<id>")
class Category_ProductAPI(Resource):
    @ns.marshal_with(Category_model)
    def get(self, id):
      return Category.query.get(id)

    @ns.expect(Category_input_model)
    @ns.marshal_with(Category_model)
    def put(self, id):
      category = Category.query.get(id)
      category.name = ns.payload["name"]
      category.description = ns.payload["description"]
      db.session.commit()
      return category

    def delete(self, id):
      category = Category.query.get(id)
      db.session.delete(category)
      db.session.commit()
      return {}, 204


@ns.route("/products")
class ProductListAPI(Resource):
  @ns.marshal_list_with(Item_model)
  def get(self):
    return Item.query.all()

  @ns.expect(Item_input_model)
  @ns.marshal_with(Item_model)
  def post(self):
      item = Item(product=ns.payload["product"],   quantity_stored=ns.payload["quantity_stored"],
                 price=ns.payload["price"],
                 unit=ns.payload["unit"],
                 category_id=ns.payload["category_id"],
                 manufacture_date=datetime.strptime(ns.payload["manufacture_date"],"%Y-%m-%d").date(),
                 expiry_date=datetime.strptime(ns.payload["expiry_date"],"%Y-%m-%d").date(),
                 description=ns.payload["description"])
      db.session.add(item)
      db.session.commit()
      return item, 201


@ns.route("/products/<int:id>")
class ProductAPI(Resource):
    @ns.marshal_with(Item_model)
    def get(self, id):
      product = Item.query.get(id)
      return product

    @ns.expect(Item_input_model)
    @ns.marshal_with(Item_model)
    def put(self, id):
      item = Item.query.get(id)
      item.product = ns.payload["product"]
      item.quantity_stored =ns.payload["quantity_stored"]
      item.price=ns.payload["price"],
      item.unit=ns.payload["unit"],
      item.category_id=ns.payload["category_id"],
      item.manufacture_date=datetime.strptime(ns.payload["manufacture_date"],"%Y-%m-%d").date(),
      item.expiry_date=datetime.strptime(ns.payload["expiry_date"],"%Y-%m-%d").date(),
      item.description=ns.payload["description"]
      db.session.commit()
      return item

    def delete(self, id):
      item = Item.query.get(id)
      db.session.delete(item)
      db.session.commit()
      return {}, 204