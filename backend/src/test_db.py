import sys
from pathlib import Path

# Add the src directory to the sys.path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from database_setup import create_db_and_tables

if __name__ == "__main__":
    create_db_and_tables()
