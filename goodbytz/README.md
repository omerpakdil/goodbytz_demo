# GoodBytz - Food Ordering and Management System

GoodBytz is a modern food ordering and management system. It provides separate interfaces for customers and kitchen staff, enables order tracking, and offers integration with robotic kitchen assistants.

## Features

- **User Login**: Separate login panels for customers and kitchen staff
- **Menu Management**: Ability to add, edit, and delete menu items
- **Order System**: Customers can select and order food from the menu
- **Order Tracking**: Real-time order tracking for kitchen staff
- **MQTT Integration**: Communication with robotic kitchen assistants

## Technical Infrastructure

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Asynchronous Operations**: FastAPI's asynchronous structure
- **MQTT Protocol**: Real-time communication
- **Containerization**: Docker and Kubernetes

## Installation

### Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations and load sample data
./prestart.sh

# Start the application
uvicorn app.main:app --reload
```

### Running with Docker

```bash
docker-compose up -d
```

## Usage

After starting the application, it can be accessed through the following URLs:

- **Home Page**: http://localhost:8000/
- **Menu**: http://localhost:8000/menu
- **Orders**: http://localhost:8000/orders
- **Kitchen Management**: http://localhost:8000/kitchen
- **API Documentation**: http://localhost:8000/docs

### Sample Users

The following sample users are automatically created when the application starts:

- **Admin**: 
  - Email: admin@goodbytz.com
  - Password: admin123
  - Permissions: Super user, Kitchen staff

- **Kitchen Staff**: 
  - Email: kitchen@goodbytz.com
  - Password: kitchen123
  - Permissions: Kitchen staff

- **Regular User**: 
  - Email: user@goodbytz.com
  - Password: user123
  - Permissions: Standard user

## API Documentation

To access the API documentation, visit the following address in your browser after starting the application:

```
http://localhost:8000/docs
```

## Testing

```bash
pytest
```

## License

This project is licensed under the MIT License. 