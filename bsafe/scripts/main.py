import json
import logging.config
import time
from pathlib import Path

import click
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

ERROR_LOG_FILENAME = ".bsafe-errors.log"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d "
            "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOG_FILENAME,
            "backupCount": 2,
        },
        "verbose_output": {
            "formatter": "simple",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "bsafe": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "logfile",
        ],
    },
}


@click.command()
@click.option(
    "--gui/--no-gui", show_default=True, help="Whether to display a browser or not."
)
def main(gui) -> None:
    """CLI app to automatically backup Pocket items and Raindrop.io items"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bsafe")

    # Configure browser
    options = Options()
    if not gui:
        options.add_argument("--headless=new")

    browser = Chrome(options)
    wait = WebDriverWait(browser, 10)

    logger.info("Loading credentials for Pocket")

    # Load credentials
    json_path = Path.cwd() / "configs" / "credentials" / "pocket.json"
    with json_path.open("r") as f:
        account_dict = json.load(f)

    logger.info("Loading of credentials for Pocket has been successful")
    logger.info("Trying login to Pocket")

    # Login to Pocket
    browser.get("https://getpocket.com/export")
    wait.until(ec.presence_of_element_located(("id", "field-1"))).send_keys(
        account_dict["email"]
    )
    wait.until(
        ec.element_to_be_clickable(("id", "onetrust-reject-all-handler"))
    ).click()
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, "loginform-submit").click()
    wait.until(ec.presence_of_element_located(("id", "field-2"))).send_keys(
        account_dict["password"]
    )
    browser.find_element(By.CLASS_NAME, "loginform-submit").click()

    logger.info("Login to Pocket has been successful")
    time.sleep(2)
    logger.info("Start a download of a HTML file storing Pocket items")

    # Download a HTML file
    wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Log In"))).click()
    wait.until(
        ec.visibility_of_element_located((By.LINK_TEXT, "Export HTML file"))
    ).click()

    logger.info("Download of Pocket items has been successful")
    time.sleep(2)
    logger.info("Loading credentials for Raindrop.io")

    # Load credentials
    json_path = Path.cwd() / "configs" / "credentials" / "raindrop_io.json"
    with json_path.open("r") as f:
        account_dict = json.load(f)

    logger.info("Loading of credentials for Raindrop.io has been successful")
    logger.info("Trying login to Raindrop.io")

    # Login to Raindrop.io
    browser.get("https://app.raindrop.io")
    wait.until(ec.presence_of_element_located(("name", "email"))).send_keys(
        account_dict["email"]
    )
    browser.find_element("name", "password").send_keys(account_dict["password"])
    browser.find_element(By.XPATH, "//input[@class='button-dQdc ']").click()

    logger.info("Login to Raindrop.io has been successful")
    logger.info("Start a download of a CSV file storing Raindrop.io items")

    # Download a CSV file
    wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "All"))).click()
    wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//div[@class='header-Tqac header-BQ_V']/div[6]")
        )
    ).click()
    browser.find_element(By.LINK_TEXT, "CSV").click()

    time.sleep(2)
    logger.info("Download of Raindrop.io items has been successful")

    browser.close()
