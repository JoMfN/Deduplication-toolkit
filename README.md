# Deduplication-toolkit
This toolkit enables flexible, safe, and domain-aware deduplication of structured file collections, especially suited for natural history and museum digitization projects

## 🚀 Features

- **Hash-based duplicate detection**
- **Regex-based UID filtering** to avoid false positives
- **Optional deletion module** with safety confirmation and dry-run mode
- **Priority-based filtering** using file metadata (size, creation date)
- **Modular scripts** for transparency and custom pipelines

---

## 📂 Components

### `find_duplicate_files.py`
- Scans directories
- Computes SHA256 hashes
- Generates `duplicates_report.txt`

### `refine_duplicates_by_uid.py`
- Filters detected duplicates using user-provided regex
- Example regex: `r'_+(?P<uid>[a-z0-9]+)_+'`

### `delete_duplicates.py`
- Deletes secondary duplicates after manual confirmation
- Supports dry-run for previewing deletions

### `priority_filters.py`
- Logic for choosing which duplicate to keep:
  - Oldest
  - Largest
  - Shortest filename

---

## 🧪 Usage Example

```bash
# Step 1: Find initial duplicates
python find_duplicate_files.py /data --output duplicates_report.txt

# Step 2: Refine using UID logic
python refine_duplicates_by_uid.py duplicates_report.txt -r '_+(?P<uid>[a-z0-9]+)_+' -e .txt -o filtered_duplicates_report.txt

# Step 3: Preview and confirm deletions
python delete_duplicates.py filtered_duplicates_report.txt --dry-run
```
