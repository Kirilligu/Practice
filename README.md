# Технологическая практика

## Satellite information transmitter

### Описание проекта
Проект представлет из себя сервер, цель которого имитировать прием данных со спутников в реальном времени, публикуя при этом данные в реальном времени. Данные скачиваются и обрабатываются в RINEX формат, обрабатываются и отправляются пользователю.

### Функицональность и работа проекта:
1. Данные ежедневно скачиваются в 22:00. Длаее они распаковываются, преобразуются в RINEX формат и сохраняются в отдельные папки для удобства.
2. Обработанные данные отправляются на публикацию потоком. 
3. Данные публикуются в mqtt broker по определенным станциям
4. Пользователь подключается к broker, подписывается на нужный ему приемник, чтобы получить нужные ему данные с выбранного приемника.

### Архитектура проекта
[Ссылка на схему всего проекта](https://drive.google.com/file/d/1OlB7rG7jkOeq_fTVc8vTLBUx4AEaVBn3/view?usp=drive_link).

![alt text](https://github.com/Kirilligu/Practice/blob/main/images/Main_diagram.drawio.png)


[Ссылка на схему скачивания данных](https://drive.google.com/file/d/1XxCZ5MK0IkJo-mH3qkU_-7HMMeecx9tS/view?usp=drive_link).

![alt text](https://github.com/Kirilligu/Practice/blob/main/images/Data_download.drawio.png)


[Ссылка на схему с блоками проекта](https://drive.google.com/file/d/1J4duBHj3aHXkFYD5pUBur6Nm5JhD-xi0/view?usp=drive_link).

![alt text](https://github.com/Kirilligu/Practice/blob/main/images/F_diagram.drawio.png)


### Описание архитектуры

Программа автоматически скачивает архив с zip файлами (в районе двух часов), разархивирует (5 минут) и конвертирует их в формат rnx (5 минут). 
Далее создаются демоны, каждый из которых непрерывно публикует данные о спутниках. Параллельно им главный скрипт непрерывно работает, скачивая новые архивы при необходимости. 
Также уделено внимание удалению ненужных файлов. Zip архивы удаляются после разархивации и конвертации их в rnx. Rnx файлы удаляются после скачивания новых zip файлов.


 

### Установка и запуск проекта
1. Установите репозиторий к себе на виртуальную машину
   ```
   sudo apt update
   sudo apt install git
   git clone https://github.com/Kirilligu/Practice
   ```
2. Перейдите в корневую папку
   ```
   cd Practice
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Скопируйте файлы сервисов в /etc/systemd/system/ :
   ```
   sudo cp services/*.service /etc/systemd/system/
   ```

5. Отредактируйте их, изменив данные и пути на свои
   ```
   sudo nano /etc/systemd/system/receiver.service
   sudo nano /etc/systemd/system/uploading_files.service
   ```
6. Запустите службы и проверьте их работоспособность:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable receiver.service uploading_files.service
   sudo systemctl start receiver.service uploading_files.service
   sudo systemctl status receiver.service
   sudo systemctl status uploading_files.service
   ```
7. Установите broker mqtt и запустите его
   ```
   sudo apt update
   sudo apt install mosquitto
   sudo systemctl start mosquitto
   ```
8. Установите утилиту CRX2RNX в свою виртуальную среду. Перейдите в директорию CRX2RNX и напишите
   ```
   sudo cp RNX2CRX CRX2RNX /usr/local/bin/
   ```
9. Запустите сервер fastapi
   ```
   uvicorn fastapi_server:app --host 0.0.0.0 --port 8000
   ```
Чтобы перейти на сервер укажите свой адрес, вместо 0.0.0.0 и напишите в конце /docs

10. Перейдите на сервер и укажите нужный приемник. Например:
![image](https://github.com/Kirilligu/Practice/assets/149255706/9eaf0340-d759-4fd8-927e-07071d473504)

11. Для получения данных можете воспользоваться приложением user, запустив его и подписавшись на нужный приемник
    ```
    python3 user.py
    ```

### Получить список существующих приемников 
    ```
    curl http://localhost:8000/receivers
    ```
### Узнать запущенные процессы 
    ```
    curl http://localhost:8000/running
    ```
