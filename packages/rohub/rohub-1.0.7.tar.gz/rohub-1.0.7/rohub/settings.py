import configparser
import os

# LOADING DATA FROM .ENV
config = configparser.ConfigParser()
env_path = os.path.join(os.path.dirname(__file__), os.pardir)
loaded_configs = config.read([os.path.join(env_path, ".env"), os.path.join(env_path, "env")])

# API SETTINGS

if loaded_configs:
    try:
        API_URL = config["API_SECTION"]["API_URL"]
    except KeyError as err:
        print("Incorrect or missing API address! Please provide proper .env file.")
else:
    API_URL = "https://api.rohub.org/api/"

# KEYCLOAK SETTING

if loaded_configs:
    try:
        KEYCLOAK_CLIENT_ID = config["KEYCLOAK_SECTION"]["KEYCLOAK_CLIENT_ID"]
        KEYCLOAK_CLIENT_SECRET = config["KEYCLOAK_SECTION"]["KEYCLOAK_CLIENT_SECRET"]
        KEYCLOAK_URL = config["KEYCLOAK_SECTION"]["KEYCLOAK_URL"]
    except KeyError as err:
        print("Incorrect or missing credentials for Keycloak! Please provide proper .env file.")
else:
    KEYCLOAK_CLIENT_ID = "rohub2020-public-cli"
    KEYCLOAK_URL = "https://login.rohub.org/auth/realms/rohub/protocol/openid-connect/token"
    KEYCLOAK_CLIENT_SECRET = None

# USER SETTINGS

USERNAME = None
PASSWORD = None
GRANT_TYPE = "password"

# TOKEN SETTINGS

ACCESS_TOKEN = None
ACCESS_TOKEN_VALID_TO = None
REFRESH_TOKEN = None
REFRESH_TOKEN_VALID_TO = None
TOKEN_TYPE = None
SESSION_STATE = None

# REQUESTS SETTINGS

TIMEOUT = 100
RETRIES = 30
SLEEP_TIME = 2

# ENDPOINTS SETTINGS

EXPORT_TO_ROCRATE_DEFAULT_FORMAT = "json-ld"

# AUXILIARY METHODS SETTINGS

ZENODO_FUNDERS_URL = "https://zenodo.org/api/funders/"
ZENODO_GRANTS_URL = "https://zenodo.org/api/grants/"
