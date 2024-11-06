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

    # Добавление обработчика к логеру
    logger.addHandler(handler)

    return logger


def register_data(input_file, output_file):
    """Основная функция для регистрации данных."""
    logger = setup_logging()
    first_lines = []
    last_lines = deque(maxlen=100)

    try:
        # Чтение данных из входного файла
        with open(input_file, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()  # Очищаем строку от пробелов и символов новой строки
                logger.debug(f"Чтение строки {i + 1}: {line}")

                # Сохранение первых 100 строк
                if i < 100:
                    first_lines.append(line)

                # этот код для избежания дублируемости в двух списках
                """else:
                    last_lines.append(line)"""

                # Обновление последних 100 строк
                last_lines.append(line)  # deque автоматически удалит старые элементы, если список станет больше 100


        logger.info("Чтение данных завершено успешно.")
        # print(len(last_lines))
        # Запись результата в выходной файл
        with open(output_file, 'w') as file:
            logger.debug("Начало записи в выходной файл.")
            for line in first_lines:
                file.write(line + '\n')
            for line in last_lines:
                file.write(line + '\n')

            logger.info("Запись данных завершена успешно.")

    except FileNotFoundError:
        logger.error(f"Файл не найден: {input_file}")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)


# Пример использования
if __name__ == "__main__":
    register_data('input.txt', 'output.txt')
