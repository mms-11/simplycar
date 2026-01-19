import React, { useEffect, useState } from 'react';
import { fetchVehicles } from '../../services/api';
import { Vehicle } from '../../types';

const VehicleList: React.FC = () => {
    const [vehicles, setVehicles] = useState<Vehicle[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadVehicles = async () => {
            try {
                const data = await fetchVehicles();
                setVehicles(data);
            } catch (err) {
                setError('Failed to fetch vehicles');
            } finally {
                setLoading(false);
            }
        };

        loadVehicles();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Vehicle List</h1>
            <ul>
                {vehicles.map(vehicle => (
                    <li key={vehicle.id}>
                        {vehicle.brand} {vehicle.model} ({vehicle.year})
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default VehicleList;