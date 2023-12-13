import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const InitiateApplication = ({ onInitiationIdChange }) => {
  const [error, setError] = useState(null);

  const handleInitiate = async () => {
    try {
      const response = await axios.post('http://localhost:8000/initiate', {
        // You can pass data in the request body if needed
      });

      // Communicate the initiation ID back to the parent component
      onInitiationIdChange(response.data.id);
      setError(null); // Clear any previous error
    } catch (error) {
      // Handle errors
      onInitiationIdChange(null); // Clear any previous id
      setError('Error initiating application'); // Set the error message
      console.error('Error initiating application:', error);
    }
  };

  return (
    <div>
      <button className="initiate-button" onClick={handleInitiate}>
        Initiate Application
      </button>

      {error && (
        <p style={{ color: 'red' }}>{error}</p>
      )}
    </div>
  );
};

export default InitiateApplication;
