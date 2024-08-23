# SPACE SITE!
## SPACE SITE! is a Flask-based demo site that takes you on a journey through the cosmos. Explore beautiful space images on the home page, manage user profiles, create and edit posts, and administer user data with ease. This application showcases the power and flexibility of Flask for building modern web applications.

## Key Features:
- Stunning Space Images: The home page features captivating images of the universe, galaxies, and cosmos, sourced from Unsplash to provide an immersive experience.

- User Management: Register, log in, and manage user profiles with personalized information, including profile pictures and contact details.

- Post Creation and Editing: Users can create, view, edit, and delete posts, making it easy to share thoughts and discoveries.

- Admin Options: Administrators have access to additional buttons to manage users data and users posts.

- Secure and Scalable: Built with security and scalability in mind, leveraging FastAPI's robust middleware and dependency injection systems.

- Two-Role Authentication: Implements a secure authentication system using JWT (JSON Web Tokens) for access and refresh tokens, stored in cookies to enhance security and user experience.

- MySQL Database: Utilizes a MySQL database for efficient and high-performance data handling, ensuring smooth operations even under high load.

## Installation
Clone the Repository

```bash
git clone https://github.com/Ruslan-Bagautdinov/SpaceSite_Flask.git
cd SpaceSite_Flask
```

### Install with Docker

```bash
docker-compose up --build
```


### Install without Docker

1. Clone the Repository:

```bash
git clone https://github.com/Ruslan-Bagautdinov/SpaceSite_Flask.git
cd SpaceSite_Flask
```
2. Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Dependencies:
```bash
pip install -r requirements.txt
```
4. Create a '.env' File:
Create a '.env' file in the root directory of the project and fill in the necessary values. You can use sample.env as a template. Here is an example of what the .env file should look like:
```dotenv
SECRET_KEY='your_secret_key'
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=10080
ALGORITHM=HS256

MYSQL_HOST='localhost'
MYSQL_PORT='3306'
MYSQL_DATABASE='spacesite_flask'
MYSQL_USER='mysql'
MYSQL_PASSWORD='your_postgres_password!'
MYSQL_ROOT_PASSWORD='your_postgres_root_password!'

UNSPLASH_ACCESS_KEY='your_unsplash_access_key'
```
Replace your_secret_key, your_mysql_data, and your_unsplash_access_key with your actual values.

5. Set Up the Database:
Ensure your MySQL database is running and configured according to the parameters in your .env file. Then, run the migrations to set up the database schema:

```bash
alembic upgrade head
```

6. Run the Application:
```bash
flask run
```

## Users

Two test users are added to the database. Their login information is as follows:

#### Admin User:
- Username: 
```
admin
```
- Password: 
```
123
```
#### Regular User:
- Username: 
```
user
```
- Password: 
```
123
```

Your application should now be running locally. You can access it at http://localhost:5000

## License
This project is currently unlicensed and free to use.
