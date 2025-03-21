# FoodAppBackend

This is the backend for a cloud kitchen food app built with Django. It manages kitchens, orders, customers, and delivery services.
## 📌 Installation Guide

install python version   Python 3.12.7 

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/puja-03/FoodAppBackend.git
cd FoodAppBackend

2️⃣ Create a Virtual Environment
python -m venv venv

Activate it:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Navigate to the Django Project Directory
cd foodapp

5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser  (optional)
python manage.py createsuperuser

7️⃣ Start the Server
python manage.py runserver