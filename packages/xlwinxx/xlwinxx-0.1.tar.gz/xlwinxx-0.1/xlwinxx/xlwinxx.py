from ftplib import FTP
import io
import os
import sys
from pathlib import Path
import time
import winsound


def check_ftp_for_new_files(ftp, last_files):
    current_files = set(ftp.nlst())
    new_files = current_files.difference(last_files)
    return new_files


def get():
    ftp = FTP('applepwp.beget.tech')
    ftp.login(user='applepwp_qqqq', passwd='Amdlover345!')
    ftp.encoding = 'utf-8'

    downloads_path = str(Path.home() / "Downloads")
    last_files = set(ftp.nlst())

    while True:
        method = input("Выберите метод (write или read): ")

        if method.lower() == "write":
            filename = input("Введите имя для нового файла (с расширением): ")
            remote_file_path = f'/{filename}'
            print("Введите текст для сохранения на FTP сервер. Для окончания ввода нажмите Enter на пустой строке.")
            data = ''
            line = input()
            while line:
                data += line + '\n'
                line = input()

            data_ftp = io.BytesIO(data.encode())
            ftp.storbinary(f'STOR {remote_file_path}', data_ftp)
            print(f"Файл {filename} успешно создан в корневом каталоге FTP сервера")

        elif method.lower() == "read":
            files = ftp.nlst()
            print("Список файлов на FTP сервере:")
            for idx, file in enumerate(files):
                print(f"{idx + 1}. {file}")
            choice = int(input("Выберите файл для чтения (введите номер): "))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
                data = bytearray()

                def write_data(buf):
                    data.extend(buf)

                try:
                    ftp.retrbinary(f"RETR {filename}", write_data)
                    content = data.decode('utf-8')
                    print(f"Содержимое файла {filename}:")
                    print(content)
                    print(f"Файл {filename} успешно скачан с FTP сервера")


                    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

                except Exception as e:
                    print(f"Ошибка при скачивании файла: {e}")
            else:
                print("Неверный выбор файла.")
        else:
            print("Неверный метод. Пожалуйста, выберите write или read.")

        time.sleep(5)
        new_files = check_ftp_for_new_files(ftp, last_files)
        if new_files:
            print(f"Новые файлы на FTP сервере: {', '.join(new_files)}")
            last_files.update(new_files)

            winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

    ftp.quit()


get()
input("Press Enter to exit...")
