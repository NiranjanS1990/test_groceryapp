from grocery import app,db,api
from grocery import models
from grocery import routes
from grocery.api_routes import ns
api.init_app(app)
#api = Api(app, prefix='/api')
api.add_namespace(ns)
with app.app_context():
    db.create_all()

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)