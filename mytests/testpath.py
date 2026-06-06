from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DBT_DIR = PROJECT_ROOT / "retail_dbt"

print(PROJECT_ROOT)