"""
migrate_to_postgres.py
======================
Run this script ONCE after you have set up your PostgreSQL database
and configured DATABASE_URL (or DB_* env vars) in your environment.

Usage:
    python migrate_to_postgres.py

What it does:
    1. Runs all Django migrations on the PostgreSQL database
    2. Loads the data_backup.json fixture (exported from SQLite)
    3. Prints a verification summary

Prerequisites:
    - DATABASE_URL or DB_* env vars must be set
    - data_backup.json must exist (created by: python manage.py dumpdata ...)
"""

import os
import sys
import subprocess


def run(cmd, **kwargs):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result


def main():
    # Ensure we're running from the correct directory
    manage = os.path.join(os.path.dirname(__file__), 'manage.py')
    python = sys.executable

    print("=" * 60)
    print("  Bakery Platform — SQLite → PostgreSQL Migration")
    print("=" * 60)

    # Step 1: Run migrations
    print("\n[1/3] Running migrations on PostgreSQL...")
    run([python, manage, 'migrate', '--run-syncdb'])

    # Step 2: Load data
    backup_file = os.path.join(os.path.dirname(__file__), 'data_backup.json')
    if os.path.exists(backup_file):
        print("\n[2/3] Loading data from data_backup.json...")
        run([python, manage, 'loaddata', backup_file])
    else:
        print("\n[2/3] SKIPPED — data_backup.json not found.")
        print("      If you have data to migrate, run first:")
        print("      python manage.py dumpdata --natural-foreign --natural-primary "
              "--exclude=contenttypes --exclude=auth.permission --indent=2 > data_backup.json")

    # Step 3: Verify
    print("\n[3/3] Running system check...")
    run([python, manage, 'check'])

    print("\n" + "=" * 60)
    print("  Migration complete! Your PostgreSQL database is ready.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Start the server:  python manage.py runserver")
    print("  2. Create a superuser if needed:  python manage.py createsuperuser")
    print("  3. Collect static files for production:  python manage.py collectstatic")


if __name__ == '__main__':
    main()
