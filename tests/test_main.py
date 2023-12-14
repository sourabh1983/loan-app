from unittest.mock import patch
from fastapi.testclient import TestClient

from loan_app.models import BusinessDetail, BalanceSheetSummary
from main import app

client = TestClient(app)


@patch("services.accounting_clients.generate_fake_balance_sheet")
@patch("services.decision_engine.get_application_result")
def test_integration(mock_decision_engine, mock_balance_sheet):
    # Mocking the accounting client to avoid actual API calls during testing
    mock_decision_engine.return_value = 100
    mock_balance_sheet.return_value = [
        {"year": 2022, "month": 9, "profit_or_loss": 874374, "assets_value": 93569}
    ]

    # Initiate application
    response = client.post("/initiate")

    assert response.status_code == 200
    assert response.json() == {"id": 0, "status": "INITIATE"}

    applicant_detail = {
        "business_name": "SKB",
        "loan_amount": 123000,
        "accounting_provider": "xero",
        "application_id": 0,
    }

    # Review Application
    response = client.post("/review_application", json=applicant_detail)

    assert response.status_code == 200
    assert response.json() == {
        "accounting_provider": "xero",
        "application_id": 0,
        "business_name": "SKB",
        "year_established": None,
        "id": 0,
        "loan_amount": 123000.0,
        "balance_sheet": [
            {"assets_value": 93569, "month": 9, "profit_or_loss": 874374, "year": 2022}
        ],
    }

    # Submit Application
    response = client.post("/submit_application/0")

    assert response.status_code == 200
    assert response.json() == {"loan_approval_amount": 100.0}
    mock_decision_engine.assert_called_once_with(
        BusinessDetail(
            name='SKB',
            year_established=None,
            requested_loan_amount=123000.0,
            balance_sheet_summary=[
                BalanceSheetSummary(
                    year=2022, profit_or_loss=874374, average_assets_value=7797.4
                )
            ],
            pre_assessment_value=60
        )
    )
