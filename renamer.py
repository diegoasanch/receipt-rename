import os
import re
import sys
import PyPDF2
from typing import Optional

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def extract_date_and_amount(pdf_path: str) -> Optional[str]:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        # Extract the first date after "Domicilio:"
        date_match = re.search(r'Domicilio:\s*(\d{2}/\d{2}/\d{4})', text)
        if not date_match:
            print("Date not found")
            return None
        date = date_match.group(1)
        day, month, year = date.split('/')

        # Updated regex to extract the amount before "Subtotal: $"
        amount_match = re.search(r'(\d+,\d{2})Subtotal:\s\$', text)
        if not amount_match:
            print("Amount not found")
            return None
        amount = amount_match.group(1).replace('.', '').replace(',', '.')
        amount_float = float(amount)

        # Format amount as "10k" if >= 10_000
        if amount_float >= 10_000:
            amount_str = f"{int(amount_float / 1_000)}k"
        else:
            amount_str = str(int(amount_float))

        month_name = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        base_name = f"{month_name[month]}_{day}_{year}_{amount_str}_ars.pdf"
        return base_name

def rename_files_in_directory(files_path: str):
    name_counter = {}
    for filename in os.listdir(files_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(files_path, filename)
            base_name = extract_date_and_amount(file_path)
            if not base_name:
                print('Skipping file:', filename, '- No name extracted')
                continue

            # Check for name collisions and add a counter if necessary
            if base_name not in name_counter:
                name_counter[base_name] = 0
            else:
                name_counter[base_name] += 1

            new_name = base_name
            if name_counter[base_name] > 0:
                base_name_without_ext, ext = os.path.splitext(base_name)
                new_name = f"{base_name_without_ext}-{name_counter[base_name]}{ext}"

            new_file_path = os.path.join(files_path, new_name)
            os.rename(file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_name}'")

def main():
    if len(sys.argv) < 2:
        eprint("No directory path provided.")
        sys.exit(1)

    files_path = sys.argv[1]
    rename_files_in_directory(files_path)

if __name__ == "__main__":
    main()
