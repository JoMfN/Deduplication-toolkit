import argparse
import os
import sqlite3
from datetime import datetime
import hashlib

def init_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS duplicates (
            hash TEXT,
            path TEXT,
            size INTEGER,
            ctime TEXT,
            error TEXT
        );
    ''')
    con.commit()
    return con

def parse_report(report_path):
    duplicates = {}
    current_hash = None
    with open(report_path, 'r') as f:
        for line in f:
            if line.startswith("Filtered") or line.startswith("Duplicate"):
                current_hash = line.strip().split()[-1][:-1]
                duplicates[current_hash] = []
            elif line.strip().startswith('/'):
                duplicates[current_hash].append(line.strip())
    return duplicates

def insert_metadata(cur, file_path, file_hash):
    try:
        stat = os.stat(file_path)
        cur.execute('''
            INSERT INTO duplicates (hash, path, size, ctime, error)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_hash, file_path, stat.st_size,
              datetime.fromtimestamp(stat.st_ctime).isoformat(), None))
    except Exception as e:
        cur.execute('''
            INSERT INTO duplicates (hash, path, size, ctime, error)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_hash, file_path, None, None, str(e)))

def log_to_sqlite(report_file, db_path):
    con = init_db(db_path)
    cur = con.cursor()
    parsed = parse_report(report_file)
    for hash_val, files in parsed.items():
        for file_path in files:
            insert_metadata(cur, file_path, hash_val)
    con.commit()
    con.close()
    print(f"Logged metadata to {db_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Store duplicate metadata in SQLite DB.')
    parser.add_argument('report', help='Duplicate report to log')
    parser.add_argument('-d', '--db', default='duplicates.db', help='SQLite DB path')
    args = parser.parse_args()

    log_to_sqlite(args.report, args.db)
