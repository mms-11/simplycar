# Automotive Service Management System - Frontend

This project is a frontend application for the Automotive Service Management System, built using React and Vite. It interacts with a FastAPI backend to manage automotive services, customers, vehicles, and appointments.

## Project Structure

- `src/`: Contains the source code for the React application.
  - `main.tsx`: Entry point of the application.
  - `App.tsx`: Main application component.
  - `components/`: Contains React components for different functionalities.
    - `Customers/`: Components related to customer management.
    - `Vehicles/`: Components related to vehicle management.
    - `Services/`: Components related to service management.
    - `Appointments/`: Components related to appointment management.
  - `services/`: Contains API service functions to interact with the backend.
  - `types/`: TypeScript types used throughout the application.

## Getting Started

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd automotive-service-system/frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000` to view the application.

## Features

- Manage customers, vehicles, services, and appointments.
- Responsive design for better user experience.
- API integration with the FastAPI backend.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.