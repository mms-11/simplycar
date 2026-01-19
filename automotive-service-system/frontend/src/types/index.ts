export interface Customer {
  id: number;
  name: string;
  phone: string;
  email: string;
}

export interface Vehicle {
  id: number;
  brand: string;
  model: string;
  year: number;
  engine: string;
}

export interface Service {
  id: number;
  name: string;
  description: string;
  averageTime: number; // in minutes
  laborCost: number; // in currency
}

export interface Appointment {
  id: number;
  customerId: number;
  vehicleId: number;
  serviceId: number;
  status: string; // e.g., 'scheduled', 'completed', 'canceled'
  totalValue: number; // in currency
}