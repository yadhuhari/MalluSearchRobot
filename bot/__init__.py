import os
import logging
import time

from logging.handlers import RotatingFileHandler

# Change Accordingly While Deploying To A VPS
APP_ID = "19383278"

API_HASH = "6e6c8100d5564c59bfd82a7a86aadb95"

BOT_TOKEN = "8104015214:AAEcbWZn7r-Nrs0megN2bD-yWkPVMow0o-w"

DB_URL = "mongodb+srv://mrprincebotx:mrprincebotx@cluster0.ikmilh0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

USER_SESSION = "BQEnw-4AtlC8zlNYE1FU8rO_Obj11qdnOdA51FDK-gUT5ujX-ocqbCqSzHKCpcDQZYb-zpuyIbAILFYm4lKICXu8nwC8PpxjnrI76OEYrZLOPGqSfwEkQh55xwYtLWORp7w1bvUHAsiZjJKuIsQDOjp3tCCMrFA6j0N93e3fG53iMNdPjI2HZouRWykbbcykLI_vPG3gZEIzk1WLNwkOAo8OsC5dbQbYCtlfv_y9fOrdin1TQjpnxpv9jtVnWnx_p34Xxgbhw-8f4IM7JjqOYFeE31TVKd2kLmNON4IsbXPYBGXvAWXMJJAPX3zjGebaG7yevj6x3_8zcfwYbFq8QS2WMib1KwAAAAGqFIlDAA"

OWNER_ID = "7148439875"

ADMINS = "7148439875"
DB_CHANNELS = "-1002648543616"

UPDATE_CHANNEL = "MalluCartoonzz"


VERIFY = {}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "MalluSearchRobot.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

start_uptime = time.time()


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
