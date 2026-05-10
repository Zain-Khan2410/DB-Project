# 🍔 FoodRush — Food Delivery Management System

FoodRush is a premium Django-based food delivery platform that connects customers with local restaurants. It features a robust owner dashboard, real-time cart management, and a clean, responsive UI.

## 🚀 Quick Start (Setup on a New Laptop)

Follow these steps to get the project running on a fresh environment.

### 1. Prerequisites
- **Python 3.10+** installed.
- **PostgreSQL** (Local or Supabase) running.

### 2. Clone and Prepare Environment
Open your terminal (PowerShell or CMD) in the project root:

```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
1. Rename `.env.example` to `.env` (or create a new `.env` file).
2. Fill in your database credentials:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
*Note: The app is pre-configured to handle both local and SSL-enabled (Supabase) connections.*

### 4. Database Setup
Apply migrations to create the database schema:

```powershell
# Generate migration files (if not already present)
python manage.py makemigrations accounts restaurant orders

# Apply migrations
python manage.py migrate

# (Optional) Seed the database with dummy data
python seed_data.py
```

### 5. Create Admin Access
If you didn't use `seed_data.py`, create a superuser to access the management panel at `/admin`:

```powershell
python manage.py createsuperuser
```

### 6. Run the Application
Start the development server:

```powershell
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Key Features
- **Customer Side**: Browse restaurants, filter by category, real-time cart, and order tracking.
- **Owner Dashboard**: Manage restaurant details, menu items, and update order statuses.
- **Admin Panel**: Full control over users, restaurants, and system-wide data.
- **Responsive UI**: Optimized for mobile, tablet, and desktop with modern CSS animations.

## 📁 Project Structure
- `accounts/`: Custom user models, authentication, and profiles.
- `restaurant/`: Restaurant listings, categories, and menu management.
- `orders/`: Cart logic, checkout process, and order history.
- `static/`: CSS (Glassmorphism & modern UI), JavaScript (Ajax Cart), and Images.
- `templates/`: Clean, reusable Django templates.

## 🔧 Troubleshooting
- **SSL Error**: If you get an SSL error while connecting to a local DB, ensure `DB_SSLMODE=prefer` is set in your `.env`.
- **Static Files**: If images don't load, ensure `DEBUG=True` in `.env` or run `python manage.py collectstatic`.
