# REST API with Django REST Framework

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)

## Introduction
This is a Django REST API project template with integrated Celery and JWT authentication. It is designed to be a robust starting point for building modern web applications.

This application is intended for importing supplier products and their attributes into a database for subsequent use on the reseller's website. A separate script checks the availability of products on the supplier's website once a day and uses this data to update the stock in the reseller's database.

Additionally, the application is integrated with a Telegram bot that serves as an assistant for sales representatives. This bot can quickly provide information about products, check stock availability, and give details about upcoming delivery dates, making it a valuable tool for efficient sales operations.

## Features
- Django 3.10
- Celery for background tasks
- JWT authentication using Simple JWT
- PostgreSQL as the database
- MongoDB as the cloud storage
- Docker and Docker Compose for containerization
- REST API with Django REST Framework
- Swagger documentation with drf-yasg
- RabbitMQ as message-broker

## Requirements
- Python 3.10
- Django 5.0.6
- PostgreSQL
- Docker & Docker Compose
- Celery 5.4.0
- Simple JWT 5.3.1
- Django REST Framework 3.15.2
- Aioaiogram 3.11.0
- Pymongo 4.8.0

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/LevytskyiS/ShopAPI.git
    cd ShopAPI
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    cd store
    pip install -r requirements.txt
    ```

4. Set up the `.env` file with your environment variables:
    ```env
    <!-- Django App -->
    SECRET_KEY=secret_key
    <!-- DRF App account -->
    API_USER_USERNAME=username       
    API_USER_PASSWORD=password
    <!-- Supplier`s account -->
    USERNAME=username               
    PASSWORD_SHOP=password
    STOCK_URL=products_url
    TOKEN_URL=token_url
    <!-- PostgreSQL Database -->
    ENGINE=engine
    NAME=db_name
    USER=db_user
    PASSWORD=password
    HOST=host
    PORT=1234
    <!-- Telegram Bot -->
    TG_TOKEN=telgegram_bot_token
    <!-- MongoDB URI -->
    URI_MONGO=mongodb_uri
    ```

5. Run docker containers
    ```
    docker-compose up -d
    ```

6. Apply migrations and create a superuser (Switch to the interactive mode of the 'webapp' application container and apply the migrations; the username and the password must be the same as you defined in the .env file):
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

## Usage
- Access the admin panel at `http://127.0.0.1:8000/admin/`
- Access the API documentation at `http://127.0.0.1:8000/swagger/`

## Running Tests
To run tests, use the following command:
    ```bash
    python manage.py test
    ```