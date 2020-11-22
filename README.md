## E-Commerce Website Project

In this project, I created an amazon-like e-commerce website using Django where users can search for available products, add their own product listings, add products to their carts, and finally order products that they have added to their cart. When first visiting the application, users will have to create an account, entering rnecessary information which will then be stored in a database and used in the website.

# Files
In total there are 23 main files used to create this website, including 6 .py files, 14 .html files, 2 .js files, and 1 .css file.
.py:
- admin.py          -> contains code to upload the databse to the admin website
- apps.py           -> contains the application name
- models.py         -> contains the database models used to create the website
- tests.py          -> contains tests for testing the website
- urls.py           -> contains the paths available in the website
- views.py          -> contains back-end python code for processing data and rendering html pages

.html:
- add.html          -> displays a form that lets the user add a new listing
- cart.html         -> displays the contents of the user's cart
- categories.html   -> displays the available product categories
- category.html     -> displays the available listings in the specified category
- checkout.html     -> displays a form that lets the user enter order information and create an order
- index.html        -> main page when the user first enters the website, displays all the available listing
- layout.html       -> layout .html file that all other .html files extend from
- listing.html      -> displays the details of a specified listing
- login.html        -> displays a form that lets the user login using their credentials
- order.html        -> displays the details of a specified order
- orders.html       -> displays all the user's orders
- profile.html      -> displays the user's profile page which contains some user info and all their listings
- register.html     -> displays a form that lets new users register an account to access the website
- search.html       -> displays the results of the listings available from the user's search query

.js:
- cart.js           -> contains front-end javascript code to manipulate cart.html's DOM and update database information
- listing.js        -> contains front-end javascript code to manipulate listing.html's DOM and update database information

.css:
- styles.css        -> contains styles used by HTML elements