from abc import ABC, abstractmethod
from typing import List
from faker import Faker
from loan_app.models import ApplicantDetail, BalanceSheet


class AccountingClient(ABC):
    @abstractmethod
    def get_balance_sheet(self):
        pass


class Xero(AccountingClient):
    def get_balance_sheet(self) -> List[BalanceSheet]:
        # Generate a fake balance sheet for now. Eventually replace with actual HTTP calls
        fake_balance_sheet = generate_fake_balance_sheet()
        return fake_balance_sheet


class Myob(AccountingClient):
    def get_balance_sheet(self) -> List[BalanceSheet]:
        # Generate a fake balance sheet for now. Eventually replace with actual HTTP calls
        fake_balance_sheet = generate_fake_balance_sheet()
        return fake_balance_sheet


def generate_fake_balance_sheet() -> List[BalanceSheet]:
    # Use the faker library to generate fake balance sheet data
    fake = Faker()
    fake_balance_sheet = [
        BalanceSheet(
            year=2023,
            month=month,
            profit_or_loss=fake.random_number(digits=6),
            assets_value=fake.random_number(digits=5),
        )
        for month in range(1, 13)
    ]
    return fake_balance_sheet


class AccountingClientFactory:
    CLIENTS = {
        "xero": Xero,
        "myob": Myob,
        # Add more entries as new accounting clients are introduced
    }

    @staticmethod
    def create_accounting_client(applicant: ApplicantDetail) -> AccountingClient:
        accounting_provider = applicant.accounting_provider.lower()
        client_class = AccountingClientFactory.CLIENTS.get(accounting_provider)
        if client_class:
            return client_class()
        else:
            raise ValueError("Unsupported accounting system")
