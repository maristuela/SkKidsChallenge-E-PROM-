import threading
import logging
from logging.handlers import RotatingFileHandler
from collections import deque

def setup_logging():
    """Настройка системы логирования."""
    logger = logging.getLogger('DataRegistrationLogger')
    logger.setLevel(logging.DEBUG)
    # Настройка ротации файла логов
    handler = RotatingFileHandler('data_registration.log', maxBytes=5 * 1024 * 1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # Добавление обработчика к логгеру
    logger.addHandler(handler)
    return logger

# Глобальные переменные
logger = setup_logging()
code_lines = []
lines_lock = threading.Lock()
first_lines = []
last_lines = deque(maxlen=100)
output_file = 'output.txt'

# Функция для ввода строк в список
def input_code_lines():
    global code_lines
    while True:
        line = input("Введите строку кода (или 'finished' для выхода): ")
        if line.lower() == 'finished':
            logger.info("Закончен цикл зарядки.")
            # Запись результата в выходной файл
            with open(output_file, 'w') as file:
                logger.debug("Начало записи в выходной файл.")
                file.write('\n'.join(first_lines) + '\n')
                logger.info("Запись данных завершена успешно.")
            break
        with lines_lock:  # Защищаем доступ к списку
            code_lines.append(line)
            # print(f"Строка добавлена: {line}")

# Функция для получения и обнуления списка
def retrieve_and_clear_lines():
    global code_lines
    while True:
        with lines_lock:  # Защищаем доступ к списку
            if code_lines:
                # print("Накопленные строки:")
                for line in code_lines:
                    line = line.strip()  # Очищаем строку от пробелов и символов новой строки
                    # print(line)
                    logger.debug(f"Чтение строки: {line}")
                    # Сохранение первых 100 строк только если это необходимо
                    if len(first_lines) < 100:
                        first_lines.append(line)
                        # этот код для избежания дублируемости в двух списках
                    """else:
                        last_lines.append(line)"""
                    # Обновление последних 100 строк
                    last_lines.append(line)  # deque автоматически удалит старые элементы, если список станет больше 100

                # print(len(first_lines))
                code_lines.clear()  # Очищаем список
                # print("Список очищен.")

def register_data():
    """Основная функция для регистрации данных."""
    # Создаем потоки
    input_thread = threading.Thread(target=input_code_lines)
    retrieve_thread = threading.Thread(target=retrieve_and_clear_lines)
    # Запускаем потоки
    input_thread.start()
    retrieve_thread.start()
    # Дожидаемся завершения потоков
    input_thread.join()
    retrieve_thread.join()

# Пример использования
if __name__ == "__main__":
    register_data()
