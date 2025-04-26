# 🏢 SaaS Real Estate CRM

A multi-tenant system built with Django for managing clients, properties, and users in real estate companies. Ideal for businesses looking to offer CRM as a service with tenant data isolation.

## 🚀 Features

- **Multi-Tenant with PostgreSQL**: Uses separate schemas for each client, ensuring data security and isolation.
- **User Management**: Role-based access control using Django Groups (admin, realtor, HR).
- **Property Management**: Create, update, and list real estate properties.
- **Admin Dashboard**: Interface to manage clients and users.
- **Authentication & Authorization**: Secure login with permission control based on groups.

## 🛠️ Technologies Used

- **Backend**: Django 4.x
- **Database**: PostgreSQL (with schema support for multi-tenancy)
- **Frontend**: HTML, CSS, SCSS, JavaScript
- **Dependency Management**: `requirements.txt`
- **Production Server**: Gunicorn

## Note
- **The Database must be PostgreSQL due to the use of schemas**


## ⚙️ Setup & Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/gabriel-melgaco/SaaS_CRM_Real_Estate.git
   cd SaaS_CRM_Real_Estate
   ```

2. **Create a virtual environment **
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Create a `.env` file in the root directory.
   - Add the following:
   ```.env
    SECRET_KEY = 'YOUR_DJANGO_SECRET_KEY'

    #DATABASE CONFIG
    DATABASE_NAME = 'YOUR_DATABASE_NAME'
    DATABASE_USER = 'YOUR_DATABASE_USER'
    DATABASE_PASSWORD = 'YOUR_DATABASE_PASSWORD'
    DATABASE_HOST = 'YOUR_DATABASE_HOST'
    DATABASE_PORT = '5432'

    #RECAPTCH CONFIG
    RECAPTCHA_PUBLIC_KEY = 'YOUR_RECAPTCHA_PUBLIC_KEY'
    RECAPTCHA_PRIVATE_KEY = 'YOUR_RECAPTCHA_PRIVATE_KEY'

    #DOMAIN NAME CONFIGS
    DOMAIN_NAME = 'localhost:5000' OR 'YOUR_DOMAIN_NAME'(PRODUCTION)

    #EMAIL CONFIGS
    FROM_EMAIL = 'YOUR_EMAIL_ADDRESS'
    ```
    - Create a 'sendgrid.env' file in the root directory for sendgrid Twillio API
    ```sendgrid.env
    export SENDGRID_API_KEY = 'YOUR_SENDGRID_API_KEY'
    ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py migrate_schemas --shared
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Django Tenant Complements Configs:**
   - access the django shell
   ```bash
   python manage.py shell
   ```
   - import the tenant complement:
   ```bash
   from public_app.models import Client, Domain  # Ajuste o nome do app conforme sua estrutura

    # Create a tenant associated with the hostname "localhost"
    tenant = Client(schema_name='public', 
                    company_name='Admin Global', 
                    paid_until='2026-01-01', 
                    on_trial=False, 
                    dns_name='localhost', 
                    telephone='123456789', 
                    activation=True)
    tenant.save()
    ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

