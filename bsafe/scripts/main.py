import click
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


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
    browser.close()
