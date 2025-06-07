import argparse
import json
import os
import hashlib
from datetime import datetime

def build_metadata_entry(filepath):
    """Extract metadata for a file."""
    try:
        stat = os.stat(filepath)
        return {
            "path": filepath,
            "size": stat.st_size,
            "ctime": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "hash": hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
        }
    except Exception as e:
        return {"path": filepath, "error": str(e)}

def parse_report(path):
    """Parses report and groups files by hash."""
    data = {}
    current_hash = None
    with open(path, 'r') as f:
        for line in f:
            if line.startswith("Filtered") or line.startswith("Duplicate"):
                current_hash = line.strip().split()[-1][:-1]
                data[current_hash] = []
            elif line.strip().startswith('/'):
                data[current_hash].append(line.strip())
    return data

def build_json_log(report_file, output_file):
    parsed = parse_report(report_file)
    output = {}
    for hash_val, files in parsed.items():
        output[hash_val] = [build_metadata_entry(f) for f in files]

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"JSON metadata log written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log duplicate metadata to JSON.')
    parser.add_argument('report', help='Path to duplicate report')
    parser.add_argument('-o', '--output', default='duplicate_metadata.json', help='Output JSON path')
    args = parser.parse_args()

    build_json_log(args.report, args.output)
