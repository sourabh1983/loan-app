from typing import List, Optional

from pydantic import BaseModel


class Application(BaseModel):
    id: Optional[int] = None
    status: str


class BalanceSheet(BaseModel):
    year: int
    month: int
    profit_or_loss: int
    assets_value: int


class BalanceSheetSummary(BaseModel):
    year: int
    profit_or_loss: int
    average_assets_value: float


class ApplicantDetail(BaseModel):
    id: Optional[int] = None
    business_name: str
    year_established: Optional[int] = None
    loan_amount: float
    accounting_provider: str
    application_id: int  # Foreign key to Application


class ApplicationReview(ApplicantDetail):
    balance_sheet: Optional[List[BalanceSheet]] = None


class BusinessDetail(BaseModel):
    name: str
    year_established: Optional[int] = None
    requested_loan_amount: float
    balance_sheet_summary: List[BalanceSheetSummary]
    pre_assessment_value: int
