import React, { useState } from 'react';
import InitiateButton from './InitiateApplication';
import LoanForm from './LoanForm';
import LoanReview from './LoanReview';

function App() {
  const [initiationId, setInitiationId] = useState(null);
  const [loanData, setLoanData] = useState(null);

  const handleInitiationIdChange = (newInitiationId) => {
    setInitiationId(newInitiationId);
  };

  const handleLoanFormSubmit = (newLoanData) => {
    setLoanData(newLoanData);
  };

  return (
    <div className="App">
      <h1>Loan Application System</h1>

      {initiationId !== null && (
        <div className="initiation-id-container">
          <p className="initiation-id">Loan Application ID: {initiationId}</p>
        </div>
      )}

      {initiationId && !loanData ? (
        <LoanForm initiationId={initiationId} onLoanFormSubmit={handleLoanFormSubmit} />
      ) : null}

      {loanData && (<div className="loan-details-container">
            <LoanReview loanData={loanData} />
          </div>
            )}

      {!initiationId && (
        <InitiateButton onInitiationIdChange={handleInitiationIdChange} />
      )}
    </div>
  );
}

export default App;

