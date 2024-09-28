import logging

AUTHORIZATION_TOKEN = "sisecam-poc-api-token"
API_URL = "https://sisecam-poc-law-backend-gbbhc6dshuegbzhp.westeurope-01.azurewebsites.net/chat"

# Logging Configuration
logger = logging.getLogger('PoC')
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
app_logger = logger
