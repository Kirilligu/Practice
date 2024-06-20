FROM python:3.9-slim

# Установка рабочего каталога
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install -r requirements.txt

# Копирование исходных файлов
COPY uploading_files.py .

# Команда для запуска скрипта
CMD ["python", "uploading_files.py"]

