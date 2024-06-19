import sys
import requests
from datetime import datetime, timedelta
import zipfile
import gzip
import os

date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

link = f"https://api.simurg.space/datafiles/map_files?date={date}"
file_name = f"{date}.zip"

with open(file_name, "wb") as f:
    print(f"Скачивание {file_name}")
    response = requests.get(link, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None: 
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
            sys.stdout.flush()
print("\nСкачивание завершено")

# Распаковка zip-файла
with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall(date)
print(f"Распаковано {file_name} в {date}/")

# Декомпрессия файлов .gz
for root, dirs, files in os.walk(date):
    for file in files:
        if file.endswith(".gz"):
            gz_file_path = os.path.join(root, file)
            output_file_path = os.path.join(root, file[:-3])    # Удаление расширения .gz
            with gzip.open(gz_file_path, 'rb') as gz_file:
                with open(output_file_path, 'wb') as out_file:
                    out_file.write(gz_file.read())

print("Декомпрессия завершена")
