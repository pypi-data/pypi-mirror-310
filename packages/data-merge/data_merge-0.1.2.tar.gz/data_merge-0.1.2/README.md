# data_merge

`data_merge` is a Python package designed for effortlessly merging multiple Excel (`.xlsx`) or CSV files into a single consolidated file. Whether you need to combine financial reports, datasets, or logs, `data_merge` simplifies the process with minimal setup.

## Features
- Merge multiple Excel files in a folder into a single file.
- Merge multiple CSV files in a folder into a single file.
- Automatically handles indexing and preserves data integrity.

## Usage Example

```python
from data_merge.file_merger import FileMerger

# Define folder path and output path
folder_path = "path/to/your/files"
output_path = "path/to/save/merged_file.xlsx"

# Merge Excel files
merger = FileMerger(folder_path, output_path)
merger.merge_excel_files()

# Merge CSV files
merger.merge_csv_files()
```

## Installation
```pip install data_merge```

## Requirements
- Python 3.x
- Pandas

## Author
Developed by Ojo Ilesanmi. Reach out at ojoilesanmi89@gmail.com.
