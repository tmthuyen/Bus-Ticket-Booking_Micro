# 🛍️ Bus Ticket Booking

A microservices-based bus booking system built with FastAPI, React, MySQL, RabbitMQ, and Docker. The platform includes user authentication, trip management, booking flows, payment processing, and notification services coordinated through an API gateway.

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Notes](#database-notes)

## 🧩 Tech Stack

- Backend: Python, FastAPI
- Frontend: React, JavaScript, MUI, Ant Design
- Databases: MySQL (separate database per service)
- Messaging: RabbitMQ
- API Gateway: FastAPI-based gateway service
- Containerization: Docker, Docker Compose
- Authentication: JWT

## 📁 Project Structure

```text
bus-ticket-booking/
├── .env
├── docker-compose.yml
├── Readme.md
├── BE/
│   ├── gateway/
│   ├── user_service/
│   ├── trip_service/
│   ├── booking_service/
│   ├── payment_service/
│   └── notify_service/
├── database/
│   ├── backup/
│   ├── desgin-db/
│   └── test-db/
└── FE/
    └── busbooking/
```

### Backend services

- `gateway`: routes public requests to internal microservices
- `user_service`: authentication, profile, and user management
- `trip_service`: trip and route management
- `booking_service`: booking creation and order processing
- `payment_service`: payment handling and transaction logic
- `notify_service`: email and notification processing using RabbitMQ

### Frontend

- `FE/busbooking`: React application for customer interaction

## ✅ Prerequisites

Before running the project, make sure the following tools are installed on your machine:

- Docker Desktop or Docker Engine
- Docker Compose
- Node.js 18+ and npm
- Git

## 🔧 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd bus-ticket-booking
```

2. Install frontend dependencies:

```bash
cd FE/busbooking
npm install
```

3. Start the backend services from the project root:

```bash
docker compose -p bus-ticket-booking up --build
```

> Run with `--build` on the first startup or after dependency or environment changes.

## ⚙️ Configuration

The project already includes a root `.env` file with environment variables for services, ports, JWT, MySQL, RabbitMQ, and SMTP.

### Key configuration values

- Gateway: `http://localhost:8000`
- User service: `http://localhost:8001`
- Trip service: `http://localhost:8002`
- Booking service: `http://localhost:8003`
- Payment service: `http://localhost:8004`
- Notification service: `http://localhost:8005`

### Important ports

- Internal service ports: `8000` for each backend service inside Docker
- External ports exposed to local machine:
  - User: `8001`
  - Trip: `8002`
  - Booking: `8003`
  - Payment: `8004`
  - Notification: `8005`
  - Gateway: `8000`
- MySQL database ports exposed for local tools:
  - User DB: `3312`
  - Trip DB: `3313`
  - Booking DB: `3314`
  - Notification DB: `3315`
  - Payment DB: `3316`

## ▶️ Running the Application

### Start all services

```bash
docker compose -p bus-ticket-booking up --build
```

### Start services in the background

```bash
docker compose -p bus-ticket-booking up -d
```

### Stop services

```bash
docker compose -p bus-ticket-booking down
```

### Start frontend separately

```bash
cd FE/busbooking
npm start
```

### Example frontend connection

The frontend is configured to use the gateway at:

```text
http://localhost:8000
```

## 📚 API Documentation

### Swagger UI

- User service: `http://localhost:8001/users/docs`
- Trip service: `http://localhost:8002/trips/docs`
- Booking service: `http://localhost:8003/bookings/docs`
- Payment service: `http://localhost:8004/payments/docs`
- Notification service: `http://localhost:8005/notifications/docs`

### ReDoc

- User service: `http://localhost:8001/users/redoc`
- Trip service: `http://localhost:8002/trips/redoc`
- Booking service: `http://localhost:8003/bookings/redoc`
- Payment service: `http://localhost:8004/payments/redoc`
- Notification service: `http://localhost:8005/notifications/redoc`

### Gateway routes

Requests can be routed through the gateway using the following patterns:

- `http://localhost:8000/users/{path}`
- `http://localhost:8000/trips/{path}`
- `http://localhost:8000/bookings/{path}`
- `http://localhost:8000/payments/{path}`
- `http://localhost:8000/notifications/{path}`

## 🗄️ Database Notes

- Each microservice uses its own MySQL database.
<!-- - Database scripts and demo SQL files are stored under the `database/` folder.
- Backup data is available in `database/backup/`.
- Design/test database schemas are available in `database/desgin-db/` and `database/test-db/`. -->

For local database access, you can connect with MySQL Workbench using the exposed ports defined in `docker-compose.yml`.

Example:

```yaml
ports:
  - '3312:3306'
```

In this example, `3312` is the port used to connect from the host machine.

## 🧪 Useful Commands

```bash
# First startup

docker compose -p bus-ticket-booking up --build

# Subsequent startup

docker compose -p bus-ticket-booking up

# Stop containers

docker compose -p bus-ticket-booking down

# Remove a specific DB volume if needed

docker compose down user_db
docker volume rm bus-ticket-booking_user_db_data
docker compose up -d user_db
```

## 📌 Notes

- The frontend and backend are separated by the gateway layer.
- JWT authentication is used for protected routes.
- RabbitMQ is used for asynchronous notification and event-driven communication.
- Docker Compose provides the easiest way to run the full system locally.

---

This project is intended for local development and demonstration of a service-oriented architecture for bus ticket booking operations.
