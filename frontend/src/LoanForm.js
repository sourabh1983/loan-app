import React, { useState } from 'react';
import axios from 'axios';

const LoanForm = ({ initiationId }) => {
  const [businessName, setBusinessName] = useState('');
  const [establishmentYear, setEstablishmentYear] = useState('');
  const [loanAmount, setLoanAmount] = useState('');
  const [accountProvider, setAccountProvider] = useState('myob');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request with the form data
      const response = await axios.post('http://localhost:8000/review_application', {
        id: 0,
        business_name: businessName,
        year_established: parseInt(establishmentYear),
        loan_amount: parseInt(loanAmount),
        accounting_provider: accountProvider,
        application_id: initiationId,
      });

      // Handle the response if needed
      console.log('Backend response:', response.data);

      // Clear form fields and error state on successful submission
      setBusinessName('');
      setEstablishmentYear('');
      setLoanAmount('');
      setAccountProvider('myob');
      setError(null);
    } catch (error) {
      // Handle errors
      setError('Error submitting loan application');
      console.error('Error submitting loan application:', error);
    }
  };

  return (
    <div>
      <h2>Loan Application Form</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Business Name:
          <input
            type="text"
            value={businessName}
            onChange={(e) => setBusinessName(e.target.value)}
            required
          />
        </label>

        <br />

        <label>
          Establishment Year:
          <input
            type="number"
            value={establishmentYear}
            onChange={(e) => setEstablishmentYear(e.target.value)}
            required
          />
        </label>

        <br />

        <label>
          Loan Amount:
          <input
            type="number"
            value={loanAmount}
            onChange={(e) => setLoanAmount(e.target.value)}
            required
          />
        </label>

        <br />

        <label>
          Account Provider:
          <select
            value={accountProvider}
            onChange={(e) => setAccountProvider(e.target.value)}
          >
            <option value="myob">MYOB</option>
            <option value="xero">Xero</option>
          </select>
        </label>

        <br />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default LoanForm;
