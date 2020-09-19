import os
from dotenv import load_dotenv
from gs_quant.session import GsSession, Environment
from gs_quant.data import Dataset

# Load environment variables
load_dotenv()

# authenticate GS Session with credentials
GsSession.use(environment_or_domain=Environment.PROD, client_id=os.getenv(
    "CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), scopes=('read_product_data', 'read_financial_data'))

# Initialize datasets
dataset_online = Dataset("COVID19_ONLINE_ASSESSMENTS_NHS")
