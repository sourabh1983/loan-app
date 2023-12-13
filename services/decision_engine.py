from loan_app.models import BusinessDetail


def get_application_result(business_detail: BusinessDetail):
    # This function calls third party api called decision engine. Below is fake return
    return (
        business_detail.requested_loan_amount
        * business_detail.pre_assessment_value
        / 100
    )
