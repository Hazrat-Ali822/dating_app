## Installation and Setup

### Prerequisites
- Python 3.x
- Django 3.x or higher
- Django REST Framework
- `djangorestframework-simplejwt` for JWT authentication

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/django-dating-platform.git
   cd django-dating-platform
Install Dependencies:
You can install the required dependencies using pip:

pip install -r requirements.txt
Database Setup:
Run the following commands to set up the database:


python manage.py migrate
Create Superuser (Optional):
Create a superuser to manage users via Django admin:


python manage.py createsuperuser
Run the Development Server:
Start the Django development server:


python manage.py runserver
You can now access the application at http://127.0.0.1:8000/.

Endpoints:
/signup/: POST request to create a new user.

/login/: POST request to authenticate a user and receive a JWT token.

/discover/: GET request to discover users based on matching attributes and opposite gender if no match is found.

Example Usage (Postman):
Login:

Method: POST

URL: http://127.0.0.1:8000/login/

Body:

username: testuser

password: password123

Response: { "access": "jwt-token-here" }

User Discovery:

Method: GET

URL: http://127.0.0.1:8000/discover/

Headers: Authorization: Bearer jwt-token-here

Response: List of matched or opposite-gender users with reasons.

Technologies Used:
Django: Backend web framework.

Django REST Framework: For building the RESTful API.

JWT (JSON Web Tokens): For secure user authentication.

SQLite: Database for storing user data.

Contribution
Feel free to fork the repository and submit pull requests. Contributions are welcome
