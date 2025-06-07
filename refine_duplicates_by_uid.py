import argparse
import os
import re
import logging
from collections import defaultdict
from priority_filters import select_file_to_keep

# Setup logging
logging.basicConfig(
    filename='logs/refine_duplicates.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_uid(path, regex_pattern):
    match = re.search(regex_pattern, path)
    if match:
        return match.group('uid')
    return None

def parse_report(file_path):
    """Parses a duplicates report and groups file paths by hash."""
    duplicates = defaultdict(list)
    current_hash = None
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("Duplicate files with hash"):
                current_hash = line.strip().split()[-1][:-1]
            elif line.strip().startswith('/'):
                if current_hash:
                    duplicates[current_hash].append(line.strip())
    return duplicates

def refine_duplicates(duplicates, regex, criterion):
    """Keeps one file per UID per duplicate group based on selection rule."""
    refined = {}
    for hash_val, file_list in duplicates.items():
        uid_map = defaultdict(list)
        for f in file_list:
            uid = extract_uid(f, regex)
            if uid:
                uid_map[uid].append(f)

        keep = []
        for uid, group in uid_map.items():
            keep_one = select_file_to_keep(group, criterion)
            keep.append(keep_one)

        # Invert: store only real duplicates
        filtered = [f for f in file_list if f not in keep]
        if filtered:
            refined[hash_val] = filtered
    return refined

def save_filtered_report(refined, output_file):
    with open(output_file, 'w') as f:
        for hash_val, files in refined.items():
            f.write(f"Filtered duplicates with hash {hash_val}:\n")
            for path in files:
                f.write(f"  {path}\n")
            f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Refine duplicates by UID and priority rules.')
    parser.add_argument('report', help='Path to original duplicates_report.txt')
    parser.add_argument('-r', '--regex', required=True, help='Regex pattern to extract UID with named group "uid"')
    parser.add_argument('-e', '--ext', default='.txt', help='File extension to consider (default: .txt)')
    parser.add_argument('-c', '--criterion', default='oldest', choices=['oldest', 'largest', 'shortest_name'],
                        help='Rule for which duplicate to keep (default: oldest)')
    parser.add_argument('-o', '--output', default='filtered_duplicates_report.txt',
                        help='Output refined report path')

    args = parser.parse_args()

    duplicates = parse_report(args.report)
    refined = refine_duplicates(duplicates, args.regex, args.criterion)
    save_filtered_report(refined, args.output)

    print(f"Filtered duplicate report saved to {args.output}")
