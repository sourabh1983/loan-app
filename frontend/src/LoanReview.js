import React, {useState} from 'react';
import axios from 'axios';

const LoanReview = ({loanData}) => {
    const [submitting, setSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState(null);
    const [loanApprovalAmount, setLoanApprovalAmount] = useState(null);

    const handleSubmit = async () => {
        try {
            setSubmitting(true);

            // Make a POST request to the backend
            const response = await axios.post(`http://localhost:8000/submit_application/${loanData.application_id}`, {});

            // Handle the response if needed
            console.log('Submission response:', response.data);
            setLoanApprovalAmount(response.data.loan_approval_amount);
            // Clear errors on successful submission
            setSubmitError(null);
        } catch (error) {
            // Handle errors
            setSubmitError('Error submitting to backend');
            console.error('Error submitting to backend:', error);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div>
            <h2>Loan Details</h2>
            <p>Business Name: {loanData.business_name}</p>
            <p>Loan Amount: ${loanData.loan_amount}</p>
            <p>Accounting Provider: {loanData.accounting_provider}</p>

            <h3>Balance Sheet</h3>
            <table>
                <thead>
                <tr>
                    <th>Year</th>
                    <th>Month</th>
                    <th>Profit/Loss</th>
                    <th>Assets Value</th>
                </tr>
                </thead>
                <tbody>
                {loanData.balance_sheet.map((entry, index) => (
                    <tr key={index}>
                        <td>{entry.year}</td>
                        <td>{entry.month}</td>
                        <td>${entry.profit_or_loss}</td>
                        <td>${entry.assets_value}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            <button
                type="button"
                onClick={handleSubmit}
                disabled={submitting}
            >
                {submitting ? 'Submitting...' : 'Submit Application'}
            </button>
            {submitError && (
                <p style={{color: 'red'}}>{submitError}</p>
            )}

            {loanApprovalAmount !== null && (
            <div>
              <h3>Loan Approval Amount</h3>
              <p>${loanApprovalAmount}</p>
            </div>
      )}
        </div>
    );
};

export default LoanReview;
