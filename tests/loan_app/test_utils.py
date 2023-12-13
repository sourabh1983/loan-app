import pytest

from loan_app import utils
from loan_app.models import BalanceSheet, BalanceSheetSummary


@pytest.mark.parametrize(
    "balance_sheet, expected_result",
    [
        (
            [
                BalanceSheet(
                    year=2020,
                    month=12,
                    profit_or_loss=250000,
                    assets_value=1234,
                ),
                BalanceSheet(
                    year=2020,
                    month=11,
                    profit_or_loss=1150,
                    assets_value=5789,
                ),
                BalanceSheet(
                    year=2020,
                    month=10,
                    profit_or_loss=2500,
                    assets_value=22345,
                ),
                BalanceSheet(
                    year=2020,
                    month=9,
                    profit_or_loss=-187000,
                    assets_value=223452,
                ),
            ],
            [
                BalanceSheetSummary(
                    average_assets_value=21068.3, profit_or_loss=66650, year=2020
                )
            ],
        ),
        (
            [
                BalanceSheet(
                    year=2018,
                    month=12,
                    profit_or_loss=300,
                    assets_value=400,
                ),
                BalanceSheet(
                    year=2018,
                    month=11,
                    profit_or_loss=200,
                    assets_value=200,
                ),
                BalanceSheet(
                    year=2018,
                    month=10,
                    profit_or_loss=100,
                    assets_value=200,
                ),
                BalanceSheet(
                    year=2018,
                    month=9,
                    profit_or_loss=-150,
                    assets_value=400,
                ),
                BalanceSheet(
                    year=2017,
                    month=12,
                    profit_or_loss=200,
                    assets_value=1200,
                ),
                BalanceSheet(
                    year=2017,
                    month=11,
                    profit_or_loss=-300,
                    assets_value=1200,
                ),
            ],
            [
                BalanceSheetSummary(
                    average_assets_value=200.0,
                    profit_or_loss=-100,
                    year=2017,
                ),
                BalanceSheetSummary(
                    average_assets_value=100.0,
                    profit_or_loss=450,
                    year=2018,
                ),
            ],
        ),
    ],
)
def test_calculate_summary(balance_sheet, expected_result):
    assert expected_result == utils.calculate_summary(balance_sheet)


@pytest.mark.parametrize(
    "loan_amount, summary, expected_result",
    [
        (
            10000,
            [
                BalanceSheetSummary(
                    year=2022, profit_or_loss=-5000, average_assets_value=12000
                )
            ],
            20,
        ),
        (
            5000,
            [
                BalanceSheetSummary(
                    year=2022, profit_or_loss=2000, average_assets_value=4000
                )
            ],
            60,
        ),
        (
            15000,
            [
                BalanceSheetSummary(
                    year=2022, profit_or_loss=8000, average_assets_value=20000
                )
            ],
            100,
        ),
    ],
)
def test_get_pre_assessment(loan_amount, summary, expected_result):
    result = utils.get_pre_assessment(loan_amount, summary)
    assert result == expected_result
