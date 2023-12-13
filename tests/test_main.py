from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_initiate_application():
    response = client.post("/initiate")

    assert response.status_code == 200
    assert response.json() == {"id": 0, "status": "INITIATE"}


@patch("services.accounting_clients.generate_fake_balance_sheet")
def test_applicant_detail(mock_balance_sheet):
    # Mocking the accounting client to avoid actual API calls during testing
    mock_balance_sheet.return_value = [
        {"year": 2022, "month": 9, "profit_or_loss": 874374, "assets_value": 93569}
    ]
    applicant_detail = {
        "business_name": "SKB",
        "loan_amount": 123000,
        "accounting_provider": "xero",
        "application_id": 1,
    }

    response = client.post("/review_application", json=applicant_detail)

    assert response.status_code == 200
    assert response.json() == {
        "accounting_provider": "xero",
        "application_id": 1,
        "business_name": "SKB",
        "year_established": None,
        "id": 0,
        "loan_amount": 123000.0,
        "balance_sheet": [
            {"assets_value": 93569, "month": 9, "profit_or_loss": 874374, "year": 2022}
        ],
    }
