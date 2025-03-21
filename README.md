# IMDb Clone Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### A Modern IMDb Clone with Django & React (Work in Progress)

![localhost](./images/imdb_clone.png)

## Project Status: Actively Developing 🚧

This project is currently under active development. We're building a backend-focused, feature-rich IMDb clone that showcases best practices in backend development. The frontend is designed to complement the backend with a clean and polished interface. New features and improvements are being added regularly.

### Current Development Focus:
- Enhancing the movie rating system
- Implementing user reviews and comments
- Adding advanced search and filtering capabilities
- Improving the user interface and experience
- Implementing real-time updates using WebSockets

## Description
This is a modern IMDb clone built with Django and Django Rest Framework, featuring a robust backend API and a responsive frontend. The project showcases modern web development practices, including containerization, CI/CD, and cloud integration.

## Key Features

- **Authentication & Authorization**
  - JWT-based authentication system
  - Custom user model with email-based authentication
  - Role-based access control

- **Movie Management**
  - Comprehensive movie information storage
  - Multiple category support for each movie
  - Advanced rating system
  - Image handling with Cloudinary integration

- **Performance & Scaling**
  - Redis caching for improved performance
  - Rate limiting and throttling
  - Asynchronous task processing with Celery
  - Containerized with Docker for easy scaling

- **Security & Quality**
  - Comprehensive test coverage
  - CI/CD pipeline with GitHub Actions
  - Code quality enforcement with linting
  - Secure media handling with Cloudinary

## Tech Stack

### Backend
- Python 3.9
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT Authentication

### Storage & Caching
- Cloudinary (Media Storage)
- Redis (Caching & Message Broker)

### DevOps & Tools
- Docker & Docker Compose
- GitHub Actions
- Flake8, Black, and isort for code quality
- Pytest for testing

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
The most recent update to the project includes integrating Cloudinary for handling media storage. Now, images can be uploaded and stored securely in Cloudinary, instead of being saved locally.

## Roadmap 🗺️

### Phase 1 (Current)
- ✅ Basic movie CRUD operations
- ✅ User authentication
- ✅ Category management
- ✅ Rating system
- 🚧 User reviews and comments
- 🚧 Advanced search functionality

### Phase 2 (Upcoming)
- 📝 Watchlist feature
- 📝 User recommendations
- 📝 Social features (following, sharing)
- 📝 Advanced analytics
- 📝 Performance optimizations

### Phase 3 (Planned)
- 📝 Mobile app integration
- 📝 Real-time notifications
- 📝 AI-powered recommendations
- 📝 Content moderation system

## Contributing

We welcome contributions! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated. Please check our [Contributing Guidelines](CONTRIBUTING.md) for more details.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- IMDb for inspiration
- Django community for excellent documentation
- All contributors who help improve this project
