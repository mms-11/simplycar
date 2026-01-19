import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Adjust the base URL as needed
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCustomers = async () => {
  const response = await apiClient.get('/customers');
  return response.data;
};

export const getVehicles = async () => {
  const response = await apiClient.get('/vehicles');
  return response.data;
};

export const getServices = async () => {
  const response = await apiClient.get('/services');
  return response.data;
};

export const getAppointments = async () => {
  const response = await apiClient.get('/appointments');
  return response.data;
};

export const createCustomer = async (customerData) => {
  const response = await apiClient.post('/customers', customerData);
  return response.data;
};

export const createVehicle = async (vehicleData) => {
  const response = await apiClient.post('/vehicles', vehicleData);
  return response.data;
};

export const createService = async (serviceData) => {
  const response = await apiClient.post('/services', serviceData);
  return response.data;
};

export const createAppointment = async (appointmentData) => {
  const response = await apiClient.post('/appointments', appointmentData);
  return response.data;
};