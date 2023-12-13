from typing import List, Optional

from loan_app.db import Database
from loan_app.models import (
    Application,
    ApplicantDetail,
    BalanceSheetSummary,
    ApplicationReview,
    BusinessDetail,
)
from loan_app import utils
from services import decision_engine
from services.accounting_clients import AccountingClientFactory


class LoanAppException(BaseException):
    pass


class LoanApp:
    def __init__(self):
        self.database = Database()

    def initiate_application(self):
        application = Application(status="INITIATE")
        return self.database.create_application(application)

    def review_application_detail(self, applicant: ApplicantDetail):
        if self.database.application_exists(applicant):
            try:
                accounting_client = AccountingClientFactory.create_accounting_client(
                    applicant
                )
                balance_sheet = accounting_client.get_balance_sheet()
            except Exception as e:
                raise LoanAppException(e)
        else:
            raise LoanAppException(f"Invalid application id {applicant.application_id}")

        self.database.update_application_status(applicant, status="REVIEW")

        return self.database.create_application_review(applicant, balance_sheet)

    def submit_application(self, application_id: int):
        # try:
        application_review_detail = self.database.get_application_review_detail(
            application_id
        )

        balance_sheet_summary = self.get_balance_sheet_summary(
            application_review_detail
        )

        pre_assessment = utils.get_pre_assessment(
            application_review_detail.loan_amount, balance_sheet_summary
        )

        self.database.update_application_status(
            application_review_detail, status="SUBMITTED"
        )

        final_result = decision_engine.get_application_result(
            BusinessDetail(
                name=application_review_detail.business_name,
                year_established=application_review_detail.year_established,
                requested_loan_amount=application_review_detail.loan_amount,
                balance_sheet_summary=balance_sheet_summary,
                pre_assessment_value=pre_assessment,
            )
        )
        # except Exception as e:
        #     raise LoanAppException(e)

        return {"loan_approval_amount": final_result}

    def get_balance_sheet_summary(
        self, application_review_detail: ApplicationReview
    ) -> Optional[List[BalanceSheetSummary]]:
        applicant_detail = self.database.get_application_review_detail(
            application_review_detail.application_id
        )
        if applicant_detail:
            return utils.calculate_summary(applicant_detail.balance_sheet)
        raise Exception("Balance sheet not found")
