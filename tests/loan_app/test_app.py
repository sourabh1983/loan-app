import pytest

from loan_app.app import LoanApp
from loan_app.models import (
    Application,
    ApplicantDetail,
    ApplicationReview,
    BalanceSheet,
    BalanceSheetSummary,
    BusinessDetail,
)
from unittest.mock import patch


class TestLoanApp:
    @pytest.fixture
    def loan_app_instance(self):
        return LoanApp()

    def test_initiate_application(self, loan_app_instance):
        result = loan_app_instance.initiate_application()

        assert result.id == 0
        assert result.status == "INITIATE"
        assert loan_app_instance.database.application_data == [
            Application(id=0, status="INITIATE")
        ]

    @patch("services.accounting_clients.generate_fake_balance_sheet")
    def test_process_applicant_detail(self, mock_balance_sheet, loan_app_instance):
        # Mocking the accounting client to avoid actual API calls during testing
        mock_balance_sheet.return_value = [
            BalanceSheet(year=2022, month=9, profit_or_loss=874374, assets_value=93569)
        ]
        loan_app_instance.database.application_data = [
            Application(status="INITIAL", id=123)
        ]
        applicant = ApplicantDetail(
            business_name="SKB",
            year_established=2017,
            loan_amount=100,
            accounting_provider="myob",
            application_id=123,
        )

        result = loan_app_instance.review_application_detail(applicant)

        assert isinstance(result, ApplicationReview)
        assert result == ApplicationReview(
            id=0,
            business_name="SKB",
            year_established=2017,
            loan_amount=100.0,
            accounting_provider="myob",
            application_id=123,
            balance_sheet=[
                BalanceSheet(
                    year=2022, month=9, profit_or_loss=874374, assets_value=93569
                )
            ],
        )
        assert loan_app_instance.database.applicant_data == [
            ApplicationReview(
                id=0,
                business_name="SKB",
                year_established=2017,
                loan_amount=100.0,
                accounting_provider="myob",
                application_id=123,
                balance_sheet=[
                    BalanceSheet(
                        year=2022, month=9, profit_or_loss=874374, assets_value=93569
                    )
                ],
            )
        ]
        assert loan_app_instance.database.application_data == [
            Application(id=123, status="REVIEW")
        ]

    @patch("services.decision_engine.get_application_result")
    def test_submit_application(self, mock_decision_engine, loan_app_instance):
        loan_app_instance.database.application_data = [
            Application(status="REVIEW", id=250)
        ]
        loan_app_instance.database.applicant_data = [
            ApplicationReview(
                id=101,
                business_name="SKB",
                loan_amount=500000,
                accounting_provider="myob",
                application_id=250,
                balance_sheet=[
                    BalanceSheet(year=2021, month=8, profit_or_loss=46502, assets_value=39095),
                    BalanceSheet(year=2021, month=11, profit_or_loss=435601, assets_value=73287),
                    BalanceSheet(year=2022, month=7, profit_or_loss=756955, assets_value=38057),
                    BalanceSheet(year=2022, month=10, profit_or_loss=226855, assets_value=5732),
                ],
            )
        ]

        loan_app_instance.submit_application(application_id=250)

        mock_decision_engine.assert_called_once_with(
            BusinessDetail(
                name="SKB",
                year_established=None,
                requested_loan_amount=500000.0,
                balance_sheet_summary=[
                    BalanceSheetSummary(
                        year=2021, profit_or_loss=482103, average_assets_value=9365.2
                    ),
                    BalanceSheetSummary(
                        year=2022, profit_or_loss=983810, average_assets_value=3649.1
                    ),
                ],
                pre_assessment_value=60,
            )
        )
        assert loan_app_instance.database.application_data == [
            Application(id=250, status="SUBMITTED")
        ]
