# Rename Receipt PDFs to include the date and amount

## This script renames all the PDFs in the current directory to include the date and amount from the first page of the PDF

The format used for extracting the file name is very specific to my use case, so it may not work for you.

> [!note]
> It is recommended to run this script in a directory with a copy of the files you want to rename, as it will modify the files in place.

## Pre-requisites

- Python 3

## Usage

1. Create a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python rename.py <path-to-pdf-files-directory>
```
