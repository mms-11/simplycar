# Automotive Service Management System

This is the backend for the Automotive Service Management System, built using FastAPI. The system is designed to manage automotive services, including customers, vehicles, services, and appointments.

## Project Structure

```
automotive-service-system
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── routes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── customers.py
│   │   │   │   ├── vehicles.py
│   │   │   │   ├── services.py
│   │   │   │   └── appointments.py
│   │   │   └── dependencies.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── vehicle.py
│   │   │   ├── service.py
│   │   │   └── appointment.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── vehicle.py
│   │   │   ├── service.py
│   │   │   └── appointment.py
│   │   ├── database
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   └── utils
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── requirements.txt
│   └── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd automotive-service-system/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the FastAPI application, execute the following command:
```
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Documentation

The automatically generated API documentation can be accessed at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Features

- Manage customers (CRUD operations)
- Manage vehicles (CRUD operations)
- Manage services (CRUD operations)
- Manage appointments (CRUD operations)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.