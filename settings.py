import os
from dotenv import load_dotenv
from gs_quant.session import GsSession, Environment
from gs_quant.data import Dataset
from uk_covid19 import Cov19API

# Load environment variables
load_dotenv()

# authenticate GS Session with credentials
GsSession.use(environment_or_domain=Environment.PROD, client_id=os.getenv(
    "CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), scopes=('read_product_data', 'read_financial_data'))

# Initialise datasets
marquee_api = Dataset("COVID19_ONLINE_ASSESSMENTS_NHS")

# Initialise UK Gov SDK
filters = [
    'areaType=utla',
]
structure = {
    "date": "date",
    # "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate"
    # "cumCasesByPublishDate": "cumCasesByPublishDate",
    # "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
    # "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
}

gov_api = Cov19API(filters=filters, structure=structure)
