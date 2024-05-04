import os

# Реальный путь к директории
directory_path = "/path/to/directory"

# Относительный путь до файла из базы данных
relative_path = "/folder/file.txt"

# Объединить относительный путь с реальным путем к директории
file_path = os.path.join(directory_path, relative_path)

# Извлечь файл из хранилища
with open(file_path, 'rb') as file:
    data = file.read()
    # Далее можно использовать данные файла по вашему усмотрению
