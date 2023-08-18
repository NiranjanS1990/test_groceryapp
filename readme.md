# App Summary
  Here we have created  multi-user grocery app with store managers and other customers. we use sqlite database to store user authentication and other grocery data
# Installation requirements
  $ pip install -r requirements.txt
# Run the app
  To run the app in Termminal use command :
  $ python app.py
# Demo
  https://groceryapp-imns.onrender.com
# DB Schema Design

* ## sqllite database is in folder instance
* ## api.yml has api documentation
* ## grocery module has all backend python files
  * ### routes.py for end point routes and also act as controller of MVC architecter.
  * ### model.py as flask-sqlachemy classes for creating database models
  * ### forms.py as wtf-forms for login, logout, registration etc
  * ### rest api routes are defined in api_routes.py
  * ### rest api models for flask-restx are defined in api_models
  * ### All static files are stored in static folder
  * ### All html,css templates are stored in template folder
* ## Reqired libraries installation for running code is specified in pyproject.toml [tool.poetry.dependencies] .Note this project was created in replit.
