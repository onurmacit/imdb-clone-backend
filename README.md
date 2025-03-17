# IMDb Clone Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### A Django-based clone of IMDb with modern web technologies.

## Description
This project is a clone of the IMDb website, built using Django for the backend. It leverages modern technologies such as Django Rest Framework, JWT Authentication, Redis, and Cloudinary for media storage. This repository includes a CI pipeline with GitHub Actions, linting rules for code quality assurance, pagination, and a dynamic frontend built with HTML, CSS, and JavaScript.

## Features

- **JWT Authentication**: Users can register and authenticate using JWT.
- **Rate Limiting**: Implemented throttling with `UserRateThrottle`, `AnonRateThrottle`, and custom throttling for movie endpoints.
- **Pagination**: Pagination has been added for the movie list, enabling easy navigation through large amounts of movie data.
- **Testing**: Comprehensive tests have been written for all features to ensure the functionality and reliability of the application.
- **Dockerized Setup**: The project is containerized with Docker, making it easy to deploy and manage the application in any environment.
- **CI with GitHub Actions**: Continuous integration is set up with GitHub Actions for linting, testing, and Docker-based workflows.
- **Frontend Integration**: A dynamic frontend, displaying movie data including posters, titles, and ratings, using HTML, CSS, and JavaScript.
- **Cloudinary Integration**: Media files, especially movie posters, are stored and served via Cloudinary.

## Technologies Used

- Django 4.2
- Django Rest Framework
- PostgreSQL
- Redis
- Celery for asynchronous tasks
- JWT Authentication
- Cloudinary for media storage
- Docker
- GitHub Actions for CI
- Pytest for testing
- Flake8 for linting
- Black for code formatting
- Bootstrap 5 for responsive design
- JavaScript for frontend interactivity

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/imdb-clone.git
cd imdb-clone
```
### 2. Install dependencies
Make sure to have Python 3.9+ and Docker installed. Then install the project dependencies:
```bash
pip install -r requirements.txt
```
### 3. Create a .env file
Create a .env file in the root directory with the following content:
```bash
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```
### 4. Build and run the Docker containers
Build and run the Docker containers. This command will set up the Django application, PostgreSQL database, and Redis server.
```bash
docker-compose up --build
```
### 5. Run the migrations
Once the containers are up, run the migrations:
```bash
docker-compose exec web python manage.py migrate
```
### 6. Access the application
The application will be available at http://localhost:8000/.

### 7. Create a superuser (optional)
To access the Django admin panel, create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```
## CI/CD Process

**Continuous Integration (CI)** ensures that every code change is automatically tested and linted, maintaining code quality and preventing bugs. **Continuous Deployment (CD)** will be implemented in the future to automate the deployment process.

This project uses **GitHub Actions** to manage continuous integration (CI) and continuous deployment (CD) processes. Code quality is checked with **Flake8**, **Black**, and **isort** on every pull request. Tests are run integrated with PostgreSQL on every code update.

The CI process includes the following steps:
- Running tests.
- Linting and code quality checks.
- Testing database configurations.

For detailed CI/CD configuration, you can refer to the `.github/workflows/ci.yml` and `.github/workflows/lint.yml` files.


## Deployment

Currently, there is no deployment pipeline. This project is focused on the development and testing phase, with Dockerized local development and CI integration through GitHub Actions.

## Latest Changes
- **Pagination Added:** The movie list now supports pagination, making it easier to navigate through large datasets.
- **Movie and Rating Models:** The project now includes dedicated models for Movie and Rating with serializers for easy data handling.
- **Frontend Updates:** HTML, CSS, and JavaScript files were added for a responsive frontend displaying movie information such as titles, ratings, and posters.
- **Cloudinary Integration:** Cloudinary has been integrated for handling media uploads (movie posters) efficiently.
- **Backend Improvements:** Enhanced movie list API and improved Cloudinary upload method for seamless media storage.


## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
