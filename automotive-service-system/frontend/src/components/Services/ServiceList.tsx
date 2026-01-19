import React, { useEffect, useState } from 'react';
import { fetchServices } from '../../services/api';

const ServiceList: React.FC = () => {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getServices = async () => {
            try {
                const data = await fetchServices();
                setServices(data);
            } catch (err) {
                setError('Failed to fetch services');
            } finally {
                setLoading(false);
            }
        };

        getServices();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h2>Service List</h2>
            <ul>
                {services.map(service => (
                    <li key={service.id}>
                        <h3>{service.name}</h3>
                        <p>{service.description}</p>
                        <p>Average Time: {service.average_time} minutes</p>
                        <p>Labor Cost: ${service.labor_cost}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ServiceList;