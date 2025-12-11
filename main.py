import logging

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def main():
    logger.debug("Main start")


if __name__ == "__main__":
    main()
