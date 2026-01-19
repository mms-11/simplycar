# Automotive Service Management System

This project is an Automotive Service Management System built with FastAPI for the backend and React with Vite for the frontend. It provides a comprehensive solution for managing automotive services, including customer management, vehicle tracking, service scheduling, and appointment handling.

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

### Backend

The backend is developed using FastAPI and includes the following components:

- **app**: Contains the main application logic.
  - **api**: Defines the API routes and dependencies.
  - **models**: Contains the database models.
  - **schemas**: Defines the Pydantic schemas for data validation.
  - **database**: Manages the database connection.
  - **utils**: Contains utility functions.

- **requirements.txt**: Lists the dependencies required for the backend.

### Frontend

The frontend is developed using React and Vite, structured as follows:

- **src**: Contains the main application code.
  - **components**: Contains React components for different functionalities.
  - **services**: Contains API service functions for interacting with the backend.
  - **types**: Defines TypeScript types used throughout the application.

- **index.html**: The main HTML file for the React application.
- **package.json**: Configuration file for npm, listing dependencies and scripts.
- **tsconfig.json**: TypeScript configuration file.
- **vite.config.ts**: Configuration file for Vite.

## Getting Started

To get started with the project, follow these steps:

### Backend Setup

1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the React application:
   ```
   npm run dev
   ```

## Features

- Customer management (CRUD operations)
- Vehicle management (CRUD operations)
- Service management (CRUD operations)
- Appointment scheduling (CRUD operations)

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.