import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CustomerList from './components/Customers/CustomerList';
import VehicleList from './components/Vehicles/VehicleList';
import ServiceList from './components/Services/ServiceList';
import AppointmentList from './components/Appointments/AppointmentList';

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <h1>Automotive Service Management System</h1>
        <Routes>
          <Route path="/customers" element={<CustomerList />} />
          <Route path="/vehicles" element={<VehicleList />} />
          <Route path="/services" element={<ServiceList />} />
          <Route path="/appointments" element={<AppointmentList />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;