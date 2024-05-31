# SpaceSite_Flask

## Description

This is a demo website built with Flask. It uses JWT in cookies for authentication and a MySQL database with SQLAlchemy and Alembic. Registered users can add an avatar and additional information. The application is containerized using Docker.

## Installation

Clone the repository

```bash
git clone https://github.com/Ruslan-Bagautdinov/SpaceSite_Flask.git
```

Navigate to the directory

```bash
cd SpaceSite_Flask
```

Optional: Set the following environment variables in a `.env` file in the root directory for a custom database connection, a strong secret key, and custom token expiration limits. For random images on the home page, add your own Unsplash access key to the `.env` file.

```bash
# .env
SECRET_KEY=<your-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=<your-access-token-expire-minutes>
REFRESH_TOKEN_EXPIRE_MINUTES=<your-refresh-token-expire-minutes>
MYSQL_HOST=<your-mysql-host>
MYSQL_PORT=<your-mysql-port>
MYSQL_DATABASE=<your-mysql-database>
MYSQL_USER=<your-mysql-user>
MYSQL_PASSWORD=<your-mysql-password>
MYSQL_ROOT_PASSWORD=<your-mysql-root-password>
UNSPLASH_ACCESS_KEY=<your-unsplash-access-key>
```

Build and run the Docker containers

```bash
docker-compose up --build -d
```

Once composed, it takes time (half a minute to a minute) to wait for the database to initialize and perform further migrations and upgrades using Alembic, please be patient.

## Usage

Access the application

Open your web browser and navigate to http://localhost:5000.

## Contributing

We welcome contributions from the community. Please read our contributing guidelines before submitting a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions or need support, please contact us at ruslan3odey@gmail.com.
