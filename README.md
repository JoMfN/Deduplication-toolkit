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
## 🛠️ Features

- 🧬 Content-based duplicate detection using SHA256 hashes
- 🔍 UID-aware filtering using regex to avoid false positives
- 🗃️ Metadata logging to both JSON and SQLite for auditability
- 🧼 Safe deletion tools with dry-run and user confirmation
- ⚖️ Priority retention logic by file size, ctime, filename lengt

## 🔧 Setup

```bash
pip install -r requirements.txt
```
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

## 🧪 Example Usage 2

```bash
python find_duplicate_files.py /data --output duplicates_report.txt
python refine_duplicates_by_uid.py duplicates_report.txt -r '(?P<uid>[a-f0-9]{6,7})' -e .txt -o filtered_duplicates_report.txt
python storage/json_logger.py filtered_duplicates_report.txt
python storage/sqlite_logger.py filtered_duplicates_report.txt
python delete_duplicates.py filtered_duplicates_report.txt --dry-run
```

## 📜 License

MIT


