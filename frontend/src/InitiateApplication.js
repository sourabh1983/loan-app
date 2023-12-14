import React, {useState} from 'react';
import axios from 'axios';
import './App.css';

const InitiateApplication = ({onInitiationIdChange}) => {
    const [error, setError] = useState(null);

    const handleInitiate = async () => {
        try {
            const response = await axios.post('http://localhost:80/initiate');

            // Communicate the initiation ID back to the parent component
            onInitiationIdChange(response.data.id);
            setError(null);
        } catch (error) {
            onInitiationIdChange(null);
            setError('Error initiating application');
            console.error('Error initiating application:', error);
        }
    };

    return (
        <div>
            <button className="initiate-button" onClick={handleInitiate}>
                Initiate Application
            </button>

            {error && (
                <p style={{color: 'red'}}>{error}</p>
            )}
        </div>
    );
};

export default InitiateApplication;
