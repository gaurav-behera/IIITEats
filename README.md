## Introduction

Looking for a hassle-free way to satisfy your hunger pangs at the campus? Look no further than IIITEats - your go-to food delivery service on campus! From scrumptious meals to quick snacks, the canteens offer a wide range of dishes to suit every palate. So why wait? Place your order today and let your friends take care of the rest!

## Index

- [Introduction](#introduction)
- [Index](#index)
- [About](#about)
- [Usage](#usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [File Structure](#file-structure)
- [Authors](#authors)
- [Assumptions](#assumptions)

## About

IIITEats is a food delivery service designed exclusively for the students of International Institute of Information Technology, Hyderabad (IIIT-H). The platform allows students to order food from any canteen and have it delivered directly to their rooms.

IIITEats also provides an opportunity for students to earn money by delivering food themselves. As a student-delivery partner for IIITEats, you can earn extra cash by delivering orders to your peers on campus.

## Usage

To use IIITEats, simply navigate to our homepage and begin exploring our database. Here are a few additional tips to help you get started:

- Getting Started
    - If you're a new user, you can create an account by entering your details. 
    - Once you've created an account, you can log in using the login page.

- Ordering Food
    - On the homepage, you can access the canteens page where you can explore a list of all the canteens on the campus.
    - Each canteen has its own menu that you can browse through, and you can add items to your cart by clicking the "Add to Cart" button.
    - To make modifications to your cart, simply navigate to the cart page where you can add or remove items and update quantities.
    - After confirming the items in your cart, enter your delivery location and click the "Place Order" button to confirm your order.
    - You can view your placed orders and the status of each order from the profile menu.

- Delivering Food
    - If you're interested in delivering food to your friends, simply navigate to the available orders page where you can view a list of orders that need to be fulfilled.
    - You can take up an order by clicking the "Take Order" button and confirming that you're available to deliver the food.
    - All the orders that you've taken up can be viewed from the profile menu, where you can also update the status of each order to keep your friends informed about the delivery status.



### Prerequisites
A `python 3.9` or newer environment with `flask` and `sqlite3` installed.

Or alternatively run this command in a python environment.
```
pip install -r requirements.txt
```

### Installation

1. Extract the .zip folder.
2. To set up the database environment, navigate to the root directory and execute the python script `data.py` -
```
python data.py
```
3. Run `main.py` from the same same directory
```
python main.py
```

### File Structure
```
.
├── README.md
├── data.py
├── iiiteats.db
├── main.py
├── menu.csv
├── requirements.txt
├── static
│   ├── assets
│   │   ├── IIIT.png
│   │   ├── background.svg
│   │   ├── bike.svg
│   │   ├── cart-black.svg
│   │   ├── cart.svg
│   │   ├── delete.svg
│   │   ├── delivryboy.png
│   │   ├── image.jpeg
│   │   ├── logo.png
│   │   ├── minus.svg
│   │   ├── non-veg.png
│   │   ├── order-food.jpg
│   │   ├── plus.svg
│   │   ├── rand.jpeg
│   │   ├── random.jpeg
│   │   ├── social-fb.png
│   │   ├── social-ig.png
│   │   ├── social-twitter.png
│   │   ├── user.jpg
│   │   ├── user.png
│   │   └── veg.png
│   ├── css
│   │   ├── canteens.css
│   │   ├── cart.css
│   │   ├── delivery-details.css
│   │   ├── delivery.css
│   │   ├── footer.css
│   │   ├── homepagenavbar.css
│   │   ├── index.css
│   │   ├── login.css
│   │   ├── menu.css
│   │   ├── navbar.css
│   │   └── order-tracking.css
│   └── js
│       ├── cart.js
│       ├── delivery-details.js
│       ├── delivery.js
│       ├── menu.js
│       ├── navbar.js
│       └── order-tracking.js
└── templates
    ├── canteens.html
    ├── cart.html
    ├── cookie.html
    ├── delivery-details.html
    ├── delivery.html
    ├── footer.html
    ├── index.html
    ├── login.html
    ├── menu.html
    ├── navbar.html
    ├── order-tracking.html
    ├── privacy.html
    └── tnc.html
```

## Authors
1. Amey Karan - https://github.com/ameykaran2k22

Worked on almost entire backened and webpage functionality with python, flask and databases.

2. Gaurav Behera - https://github.com/gaurav-behera

Worked on webpages layouts and functionality with html, css, javascript and python.

3. Sujal Deoda - https://github.com/su-1042

Worked on the webpage design with html and css as well as populated data for the databases.

## Assumptions

- The login page has been implemented to allow for multiple users to use the website. However, the current implementation is not completely foolproof and may require further improvements in the future. Additionally, the logout option has not been implemented yet

- While the website is functional for the most part, there are a few edge cases that are not yet handled. For example, if the cart is empty, if no orders have been placed, or if no deliveries have been taken up, the website may not behave as expected. These cases will be addressed in future updates to make the website more robust and user-friendly.

- While the prices of the items are mentioned, the payment process has not currently been integrated.

- The filter options on the menu and delivery pages are not completely functional at the moment. While you can select and deselect the checkboxes, the filtering logic is not yet implemented. 
  

