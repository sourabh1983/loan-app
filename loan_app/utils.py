from collections import defaultdict
from typing import List

from loan_app.models import BalanceSheet, BalanceSheetSummary


def calculate_summary(balance_sheet: List[BalanceSheet]) -> List[BalanceSheetSummary]:
    summary_by_year = defaultdict(
        lambda: {"profit_or_loss": 0, "average_assets_value": 0}
    )

    for entry in balance_sheet:
        year = entry.year
        profit_or_loss = entry.profit_or_loss
        assets_value = entry.assets_value

        summary_by_year[year]["profit_or_loss"] += profit_or_loss
        summary_by_year[year]["average_assets_value"] += assets_value

    result_summary = []
    for year, data in sorted(summary_by_year.items()):
        average_assets_value = data["average_assets_value"] / 12
        result_summary.append(
            BalanceSheetSummary(
                year=year,
                profit_or_loss=data["profit_or_loss"],
                average_assets_value=round(average_assets_value, 1),
            )
        )

    return result_summary


def get_pre_assessment(loan_amount, summary: List[BalanceSheetSummary]) -> int:
    # Get the summary of the last year
    last_year_summary = summary[-1]

    if (
        last_year_summary.profit_or_loss > 0
        and last_year_summary.average_assets_value > loan_amount
    ):
        return 100
    elif last_year_summary.profit_or_loss > 0:
        return 60
    else:
        return 20
