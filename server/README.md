# BACKEND (Taxi / Ride Share Application)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Project Description

This is an early-stage Ride-Sharing application. It will be implemented using **Django REST Framework** for the Backend and **Angular** for the Frontend.

It will rely on real-time, bi-directional communication between riders and a drivers. This will be achieved with `WebSockets` and `Django Channels`.

At the end it will be possible to access both experiences simultaneously in order to see how a trip is planned and executed in real-time.

🚧 Work in progress.

## Hands On Objectives

- Create a RESTful API with Django REST Framework.
- Implement token-based authentication with JSON Web Tokens (JWT).
- Use Django Channels to create and update data on the server.
- Send messages to the UI from the server via WebSockets.
- Test asyncio coroutines with pytest.

## Estructure

The project follows the Django-Cookiecutter structure, with some modifications and additions to bring a better developer experience.

The directories `contrib`, `static`, `templates` and the different `apps` are located inside the `core` directory.

## Stack

- Django
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Docker
- Docker Compose
- Pre-commit (Code Quality must be checked before commit)

## Env Files

Environment variables for local development are included to enable easy setup for local development.

For production environments, a secret `.env` file must be created and keep it safe.

## Makefile

A Makefile is provided with the most common commands to run the project.

### 1. Setup

Build the image and start the containers (not detach mode, to see the logs in the terminal):

```bash
make up-build
```

### 2. Create Superuser and Test User in Development Environment

In a separate terminal, run the following command to create a `superuser` and a `test user` (Only works in development environment). The email and passwords can be found in the `core/users/management/commands/create_local_user_and_admin.py` file.

⚠️ To access to the API <http://127.0.0.1:8000/api/> the `admin` credentials must be provided.

```bash
make users
```

### 4. The API

Once logged in as an admin, it is possible to access it at <http://127.0.0.1:8000/api/>.
There it is possible to see the available endpoints and test them.

```json
{
    "users": "http://127.0.0.1:8000/api/users/",

}
```

### Test tests with pytest and coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
make test
```

```bash
make coverage
```

## 📧 Email Server in DEVELOPMENT

Mailpit allow us to test the email sending in development environment without sending real emails.

Container mailpit will start automatically when you will run all docker containers in development.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`
