import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

LOG_DIR = BASE_DIR / Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "lehaneos.log"

def configure_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
