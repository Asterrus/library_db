import logging
import os

logger = logging.getLogger(__name__)


def get_database_url() -> str:
    logger.debug("get_database_url")
    from dotenv import load_dotenv

    load_dotenv()
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSTGRES_PORT")
    assert all(
        [postgres_user, postgres_password, postgres_db, postgres_host, postgres_port]
    ), "Missing required database environment variables"
    url = f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    logger.debug(f"Database URL: {url}")
    return url
