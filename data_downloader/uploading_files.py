import sys
import requests
from datetime import datetime, timedelta
import zipfile
import gzip
import os
import logging
import subprocess
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataDownloader")

date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
link = f"https://api.simurg.space/datafiles/map_files?date={date}"
file_name = f"{date}.zip"


def download_file(url, file_name):
    with open(file_name, "wb") as f:
        logger.info(f"Скачивание {file_name}")
        response = requests.get(url, stream=True)
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
                output_file_path = os.path.join(root, file[:-3])
                with gzip.open(gz_file_path, 'rb') as gz_file:
                    with open(output_file_path, 'wb') as out_file:
                        out_file.write(gz_file.read())
                logger.info(f"Декомпрессирован {gz_file_path} в {output_file_path}")
                os.remove(gz_file_path)
                logger.info(f"Удален {gz_file_path}")


def decompress_z_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".z") or file.endswith(".Z"):
                z_file_path = os.path.join(root, file)
                output_file_path = os.path.join(root, file[:-2])
                try:
                    with open(z_file_path, 'rb') as f_in:
                        with open(output_file_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    logger.info(f"Декомпрессирован {z_file_path} в {output_file_path}")
                except Exception as e:
                    logger.error(f"Ошибка декомпрессии {z_file_path}: {e}")
                else:
                    if os.path.exists(z_file_path):
                        os.remove(z_file_path)
                        logger.info(f"Удален {z_file_path}")


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def convert_crx_to_rnx(directory):
    crx2rnx_path = "CRX2RNX"
    if not shutil.which(crx2rnx_path):
        logger.error(f"Команда {crx2rnx_path} не найдена. Убедитесь, что инструмент установлен и доступен в PATH.")
        sys.exit(1)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".crx"):
                crx_file_path = os.path.join(root, file)
                rnx_folder_name = file.split("_")[0]
                rnx_folder_path = os.path.join(root, rnx_folder_name)

                ensure_directory_exists(rnx_folder_path)

                command = f"{crx2rnx_path} {crx_file_path} -f -d"
                try:
                    subprocess.run(command, check=True, shell=True)
                    rnx_file_path = crx_file_path.replace(".crx", ".rnx")
                    target_rnx_file_path = os.path.join(rnx_folder_path, os.path.basename(rnx_file_path))
                    shutil.move(rnx_file_path, target_rnx_file_path)
                    logger.info(f"Конвертирован {crx_file_path} в {target_rnx_file_path}")

                    if os.path.exists(crx_file_path):
                        os.remove(crx_file_path)
                        logger.info(f"Удален {crx_file_path} после успешной конвертации и перемещения")
                except subprocess.CalledProcessError as e:
                    logger.error(f"Ошибка конвертации {crx_file_path}: {e}")
                except Exception as e:
                    logger.error(f"Ошибка перемещения файла {rnx_file_path} в {target_rnx_file_path}: {e}")


if __name__ == "__main__":
    download_file(link, file_name)
    unzip_file(file_name, date)
    decompress_gz_files(date)
    decompress_z_files(date)
    convert_crx_to_rnx(date)

    logger.info("Все файлы успешно загружены, декомпрессированы и конвертированы")
