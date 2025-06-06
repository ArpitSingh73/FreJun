# 💸 Expense Tracker API (Django REST Framework)

This is a backend API for a simple Expense Tracker application. It supports **JWT authentication**, **expense management**, and **expense analytics** with daily/weekly/monthly trends.

---

## 🚀 Features

- ✅ JWT-based authentication
- ✅ Add, list, and analyze personal expenses
- ✅ Category-wise and time-wise expense breakdown
- ✅ Secure password hashing
- ✅ Protected endpoints (requires login)

---

## 🔧 Tech Stack

- Python 3.x
- Django
- Django REST Framework (DRF)
- djangorestframework-simplejwt (for JWT authentication)
- SQLite (default) or PostgreSQL

---

## 📁 API Endpoints

### 🔐 Authentication

| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| POST   | `/api/signup/`   | Register a new user      |
| POST   | `/api/login/`    | Login, get JWT tokens    |

---

### 💰 Expenses

| Method | Endpoint           | Description                              |
|--------|--------------------|------------------------------------------|
| POST   | `/api/expenses/`   | Add a new expense (authenticated)        |
| GET    | `/api/expenses/`   | List all expenses (authenticated)        |

You can pass optional query params like `?period=daily`, `?period=weekly`, or `?period=monthly` for trends.

---

### 📊 Analytics

| Method | Endpoint                  | Description                            |
|--------|---------------------------|----------------------------------------|
| GET    | `/api/expenses/analytics/`| Get total + trends + category breakdown|

Query Params:
- `period=daily` (default)  
- `period=weekly`  
- `period=monthly`  

---

## ✅ Installation & Setup

1. **Clone the Repo**
2. **change working directory to backend_**
3. **run the command: pip install -r requirements.txt**
4. **Run py manage.py runserver**
 
