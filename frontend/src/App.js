import React, { useState } from 'react';
import InitiateButton from './InitiateApplication';
import LoanForm from "./LoanForm";

function App() {
  const [initiationId, setInitiationId] = useState(null);

  const handleInitiationIdChange = (newInitiationId) => {
    setInitiationId(newInitiationId);
  };

  return (
    <div className="App">
      <h1>Loan Application System</h1>
      {initiationId !== null && (
        <div className="initiation-id-container">
          <p className="initiation-id">Loan Application ID: {initiationId}</p>
        </div>
      )}
        {initiationId ? (
        <div>
          <LoanForm initiationId={initiationId} />
        </div>
      ) : (
        <InitiateButton onInitiationIdChange={handleInitiationIdChange} />
      )}
    </div>
  );
}

export default App;
