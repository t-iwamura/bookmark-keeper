from datetime import date, timedelta
from pathlib import Path


def manage_backup() -> None:
    """Manage backup files by removing a file saved 30 days ago"""
    expire_date = date.today() - timedelta(days=30)
    date_str = expire_date.strftime("%Y_%m_%d")
    output_dir_path = Path.cwd() / "data" / "outputs"

    old_file_path = output_dir_path / f"pocket_{date_str}.html"
    if old_file_path.exists():
        old_file_path.unlink()

    old_file_path = output_dir_path / f"raindrop_{date_str}.csv"
    if old_file_path.exists():
        old_file_path.unlink()
