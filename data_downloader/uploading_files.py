import sys
import requests
from datetime import datetime, timedelta
import zipfile
import gzip
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataDownloader")

date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

link = f"https://api.simurg.space/datafiles/map_files?date={date}"
file_name = f"{date}.zip"

def download_file(url, file_name):
    with open(file_name, "wb") as f:
        logger.info(f"Скачивание {file_name}")
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # отсутствует заголовок content-length
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
    logger.info("\nСкачивание завершено")

def unzip_file(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    logger.info(f"Распаковано {zip_file} в {extract_to}/")
    os.remove(zip_file)
    logger.info(f"Удален {zip_file}")

def decompress_gz_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".gz"):
                gz_file_path = os.path.join(root, file)
                output_file_path = os.path.join(root, file[:-3])  # Удаление расширения .gz
                with gzip.open(gz_file_path, 'rb') as gz_file:
                    with open(output_file_path, 'wb') as out_file:
                        out_file.write(gz_file.read())
                logger.info(f"Декомпрессирован {gz_file_path} в {output_file_path}")
                os.remove(gz_file_path)
                logger.info(f"Удален {gz_file_path}")

if __name__ == "__main__":
    download_file(link, file_name)

    # Распаковка zip-файла
    unzip_file(file_name, date)

    # Декомпрессия файлов .gz (включая повторную проверку в разархивированных папках)
    decompress_gz_files(date)

    logger.info("Все файлы успешно загружены и декомпрессированы")
