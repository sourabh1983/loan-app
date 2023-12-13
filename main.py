from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from loan_app.app import LoanApp, LoanAppException
from loan_app.models import Application, ApplicantDetail, ApplicationReview

app = FastAPI()
loan_app = LoanApp()

# Configure CORS
origins = [
    "http://localhost:3000",  # React app url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/initiate", response_model=Application)
def initiate_application():
    return loan_app.initiate_application()


@app.post("/review_application", response_model=ApplicationReview)
def review_application(applicant: ApplicantDetail):
    try:
        return loan_app.review_application_detail(applicant)
    except LoanAppException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/submit_application/{application_id}")
def submit_application(application_id: int):
    try:
        return loan_app.submit_application(application_id)
    except LoanAppException as e:
        raise HTTPException(status_code=400, detail=str(e))
