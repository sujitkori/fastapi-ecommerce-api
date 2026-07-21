import logging
from pathlib import Path

#Projet root folder (F:\fastapi_ecommerce)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

""" Here __file__ is a special variable which means The current file. In our case it is: 
F:\fastapi_ecommerce\app\core\logging_config.py and Path(__file__).resolve() 
Now Python converts it into a proper absolute path. Still F:\fastapi_ecommerce\app\core\logging_config.py"""

# Logs directory
LOG_DIR = BASE_DIR / "logs"

#  Create logs folder if it doesn't exist
LOG_DIR.mkdir(exist_ok = True) 
"""
Here we didn't write it like LOG_DIR.mkdir(parents=True, exist_ok=True).
I mean we didn't use parents=True becasue we only need one folder.
If we want nested folder then we have to write parents=True.
"""

# Log file path
LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    filename=str(LOG_FILE),
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)