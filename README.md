# Django Application
Hi :grinning: ! Here is my Vendor Management System with Performance Metrics created in Django 4.2.6 

click the below link to check out the app in action 😄 !   
### Note: the app in deployed in render.com free service so please expect a delay on 2min or less for app to load up

[vendormanagementapp.onrender.com](https://vendormanagementapp.onrender.com)

### Objective 
Develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics. 

### GUIDE 
Below URLs are the reference wrt to vendor profiles, track purchase orders, and calculate vendor performance metrics having CRUD operations.

- Has Token Authentication Support with token expiry of 5min and User will be directed to login Screen for fetching token.

- Login System is statically typed and doesnt involve Database as this was POC app , the username and password to login are given below
>Username : Admin
>Password : password


### Instructions to Run the application

- STEP 1 : Clone this repo in your local system
- STEP 2 : run this command , keeping project directory as root : 
>pip install -r requirements.txt

- STEP 3 : run below cmd to create migrations
>py manage.py makemigrations

- STEP 4 : run below cmd to push migrations to DB
>py manage.py migrate

- STEP 5 : run below command in terminal  to run the application
> py manage.py runserver

### Purchase Order Tracking

- GET 'api/purchase_orders' - List all purchase orders
- GET 'api/purchase_orders/(str:po_number)' - Retrieve details of a specific purchase order. 
- DELETE 'api/purchase_orders/delete/(str:po_number)' -  Delete a purchase order. 
- POST 'api/create/purchase_orders' -  Create a purchase order. 
- PUT 'api/update/purchase_orders/(str:po_number)' -  Update a purchase order. 


### Vendor Profile Management

- GET      'api/vendors' -  List all vendors.
- GET      'api/vendors/(str:vendor_code)' - Retrieve a specific vendor's details.
- DELETE 'api/vendor/delete/(str:vendor_code)' -  Delete a vendor. 
- POST    'api/create/vendor' - Create a new vendor
- PUT      'api/update/vendor/(str:vendor_code)' - Update a vendor's details. 

### Vendor Performance Evaluation

- GET 'api/vendor/delete/(str:vendor_code)/performance' -  Retrieve a vendor's performance metrics.
- POST 'api/purchase_orders/(str:vendor_code)/acknowledge' -  for vendors to acknowledge POs. 
- GET 'api/purchase_orders_acknowledgementList' - To acknowledge PO's from UI 



### main

-GET  'login' - Login Page
-GET  '' - Home Page.

### SCREEN SHOTS OF WORKING APPLICATION

![](https://github.com/praveenRI007/VendorManagementApp/blob/master/home-page.png) 

![](https://github.com/praveenRI007/VendorManagementApp/blob/master/po-acknowledgement-list.png)

![](https://github.com/praveenRI007/VendorManagementApp/blob/master/purchase-order-tracking-list.png)

![](https://github.com/praveenRI007/VendorManagementApp/blob/master/vendor-login-page.png)

![](https://github.com/praveenRI007/VendorManagementApp/blob/master/vendor-performance-evaluation.png)

![](https://github.com/praveenRI007/VendorManagementApp/blob/master/vendor-profile-list.png)


### Thank you :grinning: !!!
