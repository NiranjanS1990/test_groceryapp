## App Summary
  Here we have created  multi-user grocery app with store managers and other customers. we use sqlite database to store user authentication and other grocery data
## Installation requirements
  $ pip install -r requirements.txt
## Run the app
  To run the app in Termminal use command :
  $ python app.py
## Demo
  https://groceryapp-imns.onrender.com
## DB Schema Design
   ![Untitled (1)](https://github.com/NiranjanS1990/test_groceryapp/assets/96157145/d4e78428-06cc-481b-a136-2c8605f7d8c4)
   
   * User Table : for for storing login details, passwords are stored in hashform.
   * login_count Table : To keep track of user engagement with app
   * Category Table: To store category to which different products belong
   * Item Table: stores product details such as quantity available, price, MFDate/Expiry date etc.
   * Cart Table: stores user detailts of cart
   * cart-products Table:  stores product details to be bought by customer.
   * Order Table: stores customer details and purchace amount 
   * order-products Table:  stores products purchased details
## API Design
   REST API were created for CRUD operations to be performed on Category and Item tables. api.yml has api documentation
## Architecture
   The grocery module follows a typical web application structure. It consists of the following components:
   * Initialization: The __init__.py file handles initialization and configuration of the grocery module.
   * Models: The models.py file defines the SqlAlchemy classes that represent the database models for the grocery module.
   * Routes and Controller Logic: The routes.py file handles creating routes and contains the logic for processing requests related to the grocery module.
  * API Routes: The api_routes.py file specifically handles API routes for interacting with the grocery module.
  * Templates: The templates folder stores HTML files for rendering dynamic web pages related to the grocery module.
  * Static Files: The static folder stores static files like CSS, JavaScript, and images.
  * Database: The database.db file, located in the instance folder, stores the actual database models for the grocery module.
  * To run the web app, execute the command $ python3 app.py in the terminal. The app.py file imports the grocery module and serves as the entry point.
## Features
   Features implemented are
    ○ Admin/Store Manager login and User login
    ○ Category Management
    ○ Product Management
    ○ Buy products from one or multiple Categories
    ○ Search for Category/Product
    ○ Secure login system
    ○ Creating editing removing new sections and product lists in it
    ○ Ability to add multiple products in a cart (may or may not belong to same category
    ○ Display all the products available for a given category to the users
    ○ Ability to buy multiple products from one or multiple sections.
    ○ Ability to show out of stock for the products that are not available.
    ○ Ability to show the total amount to be paid for the transaction.
    ○ APIs for interaction with sections and products
      ■ CRUD on sections
      ■ CRUD on products
    ○ All form inputs fields - text, numbers, dates etc. with suitable flash messages
    ○ Backend validation before storing / selecting from database
    ○ Gives 20% discount on the total amount on the first purchase.
