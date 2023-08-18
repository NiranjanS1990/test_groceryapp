from flask_restx import fields
from grocery import api 


class MyDateFormat(fields.Raw):
  def format(self, value):
    return value.strftime('%Y-%m-%d')


Item_model = api.model("Item",{
  "id": fields.Integer(readonly=True,description='Category unique identifier'),
  "product": fields.String(required=True,description='Product Name'),
  "quantity_stored":fields.Integer(required=True,description='Quantity of product available in the store'),
  "price":fields.Integer(required=True,description="Unit Price of given item"),
  "unit": fields.String(required=True,description='Storage unit of given product. e.g. per Kg etc'),
  "category_id": fields.Integer(required=True,description="Foreign key indicating in which category given product belong"),
  "manufacture_date": fields.Date,
  "expiry_date": fields.Date,
  "description":fields.String(description="Breif Description of Product")
})


Category_model = api.model("Category", {
  "id": fields.Integer,
  "name": fields.String,
  "description": fields.String,
  "items": fields.List(fields.Nested(Item_model))
})

Category_input_model = api.model("CategoryInput", {
  "name": fields.String,
  "description":fields.String
})

Item_input_model = api.model("ItemInput", {
  "product": fields.String,
  "quantity_stored":fields.Integer,
  "price":fields.Integer,
  "unit": fields.String,
  "category_id": fields.Integer,
  "manufacture_date":fields.Date,
  "expiry_date":fields.Date,
  "description":fields.String
})