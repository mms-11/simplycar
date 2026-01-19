import React, { useEffect, useState } from 'react';
import { getAppointments } from '../../services/api';
import { Appointment } from '../../types';

const AppointmentList: React.FC = () => {
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchAppointments = async () => {
            try {
                const data = await getAppointments();
                setAppointments(data);
            } catch (err) {
                setError('Failed to fetch appointments');
            } finally {
                setLoading(false);
            }
        };

        fetchAppointments();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h2>Appointment List</h2>
            <ul>
                {appointments.map((appointment) => (
                    <li key={appointment.id}>
                        <p>Customer ID: {appointment.customer_id}</p>
                        <p>Vehicle ID: {appointment.vehicle_id}</p>
                        <p>Service ID: {appointment.service_id}</p>
                        <p>Status: {appointment.status}</p>
                        <p>Total Value: ${appointment.total_value}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AppointmentList;