
# E-Commerce Platform

This project is an E-Commerce platform where users can buy and sell items, similar to platforms like eBay. The website allows sellers to list products, buyers to make purchases or place bids, and admins/managers to oversee platform operations.

## Features
- User roles: Buyers, Sellers, Managers, Admins.
- Product listings: Sellers can create, update, and manage their listings.
- Bidding or direct purchase options for buyers.
- Secure user authentication & authorization.
- Shopping cart & checkout system for buyers.
- Order management and tracking.
- Reviews & ratings for products and sellers.
- Admin/Manager dashboards for managing users, products, and sales analytics.

## Technologies Used
- **Backend**: Django & Django REST Framework
- **Frontend**: React
- **Authentication**: JWT (JSON Web Token)
- **Real-time features**: Django Channels (for live bidding and notifications)
- **State Management**: Context API or Redux (React)
- **Database**: PostgreSQL (or any other relational database)
- **Payment Gateway**: Integration with Stripe or PayPal (optional)

## Collaborators
- **Yousef M. Y. AlSabbah** - Django Developer
- **Yosef G. Harara** - React Developer

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone git@github.com:HYPEXc/E-Commerce-Platform.git
   ```

2. Backend (Django):
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the Django development server:
     ```bash
     python manage.py runserver
     ```

3. Frontend (React):
   - Navigate to the frontend directory and install dependencies:
     ```bash
     npm install
     ```
   - Run the React development server:
     ```bash
     npm start
     ```
