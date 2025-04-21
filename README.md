# Food Ordering System (Django)

A Django-based web application that allows users to browse dishes, manage a cart, place orders, and for admins to manage those orders. The application includes authentication, permissions, AI-assisted dish metadata, and a clean UI with pagination and sorting.

## Features

- User registration and login
- Browse dishes by category or search
- Add/remove dishes to/from cart
- Dynamic sorting and filtering of dishes
- Order placement with payment simulation
- Admin dashboard to:
  - Add new dishes
  - Accept/reject orders
  - View all user orders
- AI-generated dish detail metadata
- Pagination support for orders
- Role-based access control (admin vs regular user)

## Technologies Used

- Django (Backend)
- SQLite (default, can be switched to PostgreSQL/MySQL)
- HTML/CSS (Templates)
- Bootstrap (for UI styling)
- Django Auth System

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/RishabhSagarTTN/restaurent.git
   cd restaurent
