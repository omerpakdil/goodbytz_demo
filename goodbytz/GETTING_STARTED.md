# Getting Started with GoodBytz

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 13 or higher
- MQTT Broker (e.g., Mosquitto)
- Docker and Docker Compose (optional)
- Kubernetes (optional)

## Development Environment Setup

### 1. Database Setup

Install PostgreSQL and create a database:

```bash
# PostgreSQL installation (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Log into PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE goodbytz;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE goodbytz TO postgres;

# Exit PostgreSQL
\q
```

### 2. MQTT Broker Setup

Install Mosquitto MQTT broker:

```bash
# Mosquitto installation (Ubuntu/Debian)
sudo apt update
sudo apt install mosquitto mosquitto-clients

# Start Mosquitto service
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

### 3. Application Setup

```bash
# Clone the project (or copy files)
git clone <repo-url> goodbytz
cd goodbytz

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Edit .env file (if necessary)
# nano .env

# Run database migrations and load sample data
chmod +x prestart.sh
./prestart.sh

# Start the application
uvicorn app.main:app --reload
```

The application should now be running at http://localhost:8000.

## Docker Setup

To run the application using Docker and Docker Compose:

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

The application should now be running at http://localhost:8000.

## Kubernetes Setup

To run the application on your Kubernetes cluster:

```bash
# Create secret
kubectl apply -f k8s/secrets.yaml

# Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# Create persistent storage
kubectl apply -f k8s/persistent-volumes.yaml

# Start database
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/db-service.yaml

# Start MQTT broker
kubectl apply -f k8s/mqtt-deployment.yaml
kubectl apply -f k8s/mqtt-service.yaml

# Start API
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml

# Configure Ingress
kubectl apply -f k8s/ingress.yaml
```

## Sample Users

When the application starts, the following sample users are automatically created:

- **Admin**: 
  - Email: admin@goodbytz.com
  - Password: admin123
  - Permissions: Super user, Kitchen staff

- **Kitchen Staff**: 
  - Email: kitchen@goodbytz.com
  - Password: kitchen123
  - Permissions: Kitchen staff

- **Normal User**: 
  - Email: user@goodbytz.com
  - Password: user123
  - Permissions: Standard user

## Troubleshooting

### Database Connection Error

If you encounter a database connection error:

1. Ensure PostgreSQL service is running: `sudo systemctl status postgresql`
2. Verify database connection settings in .env file
3. Ensure database user has the required permissions

### MQTT Connection Error

If you encounter an MQTT connection error:

1. Ensure Mosquitto service is running: `sudo systemctl status mosquitto`
2. Verify MQTT broker settings in .env file
3. Ensure Mosquitto configuration allows anonymous connections

### Other Issues

Check logs for other issues:

```bash
# Application logs
tail -f app.log

# Docker logs
docker-compose logs -f

# Kubernetes logs
kubectl logs -f deployment/goodbytz-api
``` 