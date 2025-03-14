import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

def backup_database():
    """Create a timestamped backup of the SQLite database"""
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.parent
    data_dir = root_dir / 'data'
    backup_dir = root_dir / 'backups'
    
    # Create backup directory if it doesn't exist
    backup_dir.mkdir(exist_ok=True)
    
    # Source database file
    db_file = data_dir / 'health_connect.db'
    
    if not db_file.exists():
        print("Database file doesn't exist yet")
        return False
    
    # Create timestamped backup name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'health_connect_{timestamp}.db'
    
    try:
        # Create a backup using SQLite's backup feature
        source = sqlite3.connect(str(db_file))
        dest = sqlite3.connect(str(backup_file))
        source.backup(dest)
        source.close()
        dest.close()
        print(f"Database backed up to {backup_file}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        # Fall back to file copy if SQLite backup fails
        try:
            shutil.copy2(str(db_file), str(backup_file))
            print(f"Database copied to {backup_file}")
            return True
        except Exception as e:
            print(f"Copy failed: {e}")
            return False

if __name__ == "__main__":
    backup_database()