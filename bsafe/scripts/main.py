import json
from pathlib import Path

import click
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

REPO_DIR_PATH = Path(__file__).parents[2].resolve()


@click.command()
@click.option(
    "--gui/--no-gui", show_default=True, help="Whether to display a browser or not."
)
def main(gui) -> None:
    """CLI app to automatically backup Pocket items and Raindrop.io items"""
    # Configure browser
    options = Options()
    if not gui:
        options.add_argument("--headless=new")

    browser = Chrome(options)
    browser.implicitly_wait(2.0)

    # Load credentials
    json_path = REPO_DIR_PATH / "configs" / "credentials" / "raindrop_io.json"
    with json_path.open("r") as f:
        account_dict = json.load(f)

    # Login to Raindrop.io
    browser.get("https://app.raindrop.io")
    browser.find_element("name", "email").send_keys(account_dict["email"])
    browser.find_element("name", "password").send_keys(account_dict["password"])
    browser.find_element(By.XPATH, "//input[@class='button-dQdc ']").click()

    browser.close()
