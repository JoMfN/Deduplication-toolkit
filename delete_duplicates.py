import argparse
import os
import logging

# Setup logging
logging.basicConfig(
    filename='logs/delete_duplicates.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_report(path):
    files = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip().startswith('/'):
                files.append(line.strip())
    return files

def delete_files(file_paths, dry_run=True):
    for file_path in file_paths:
        if not os.path.exists(file_path):
            logging.warning(f"File does not exist: {file_path}")
            continue
        if dry_run:
            print(f"[DRY RUN] Would delete: {file_path}")
        else:
            try:
                os.remove(file_path)
                logging.info(f"Deleted: {file_path}")
                print(f"Deleted: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete {file_path}: {e}")
                print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete duplicate files listed in a report.')
    parser.add_argument('report', help='Report file listing files to delete')
    parser.add_argument('--dry-run', action='store_true', help='Preview deletions without deleting (default)', default=True)
    args = parser.parse_args()

    file_paths = parse_report(args.report)

    print(f"\n{len(file_paths)} files marked for deletion.")
    confirm = input("Do you want to proceed with deletion? (yes/no): ").strip().lower()

    if confirm == 'yes':
        delete_files(file_paths, dry_run=args.dry_run)
    else:
        print("Deletion aborted.")
