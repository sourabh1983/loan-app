from loan_app.models import (
    Application,
    ApplicantDetail,
    BalanceSheet,
    ApplicationReview,
)
from typing import List


class Database:
    def __init__(self):
        self.application_data = []
        self.applicant_data = []

    def create_application(self, application: Application):
        application.id = len(self.application_data)
        self.application_data.append(application)
        return self.application_data[-1]

    def create_application_review(
        self, applicant: ApplicantDetail, balance_sheet: List[BalanceSheet]
    ):
        application_review = ApplicationReview(
            id=len(self.applicant_data),
            business_name=applicant.business_name,
            year_established=applicant.year_established,
            loan_amount=applicant.loan_amount,
            accounting_provider=applicant.accounting_provider,
            application_id=applicant.application_id,
            balance_sheet=balance_sheet,
        )
        self.applicant_data.append(application_review)
        return self.applicant_data[-1]

    def update_application_status(self, applicant: ApplicantDetail, status) -> None:
        for x in self.application_data:
            if x.id == applicant.application_id:
                x.status = status
                break

    def get_application_review_detail(self, application_id: int) -> ApplicationReview:
        for applicant in self.applicant_data:
            if applicant.application_id == application_id:
                return applicant

        raise Exception(
            f"Applicant with application id {application_id} does not exist"
        )

    def application_exists(self, applicant: ApplicantDetail) -> bool:
        for application in self.application_data:
            if applicant.application_id == application.id:
                return True
        return False
