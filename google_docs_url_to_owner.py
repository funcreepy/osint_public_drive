import subprocess
import threading
import logging
from queue import Queue

# Пути к файлам
input_file = "urls.txt"  # Файл с URL
output_file = "results.txt"  # Файл для записи результатов
log_file = "script.log"  # Файл для логов

# Настройка логирования
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Функция для чтения URL из файла
def read_urls(file_path):
    try:
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
        return []

# Функция для выполнения команды и получения результата
def run_xeuledoc(url, results):
    try:
        result = subprocess.run(["xeuledoc", url], capture_output=True, text=True)
        output = result.stdout
        results[url] = output
        logging.info(f"Успешно обработан URL: {url}")
    except Exception as e:
        error_message = f"Ошибка при обработке URL {url}: {e}"
        results[url] = error_message
        logging.error(error_message)

# Функция для записи результатов в файл
def write_results(file_path, results):
    with open(file_path, "w") as file:
        for url, output in results.items():
            file.write(f"URL: {url}\n{output}\n{'-'*40}\n")

# Основной блок
if __name__ == "__main__":
    urls = read_urls(input_file)
    if not urls:
        print("Нет URL для обработки.")
    else:
        results = {}
        queue = Queue()

        # Функция для обработки URL из очереди
        def worker():
            while not queue.empty():
                url = queue.get()
                if url is None:
                    break
                run_xeuledoc(url, results)
                queue.task_done()

        # Заполнение очереди URL
        for url in urls:
            queue.put(url)

        # Создание потоков
        threads = []
        num_threads = min(10, len(urls))  # Ограничение на количество потоков
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Ожидание завершения обработки
        for thread in threads:
            thread.join()

        # Запись результатов в файл
        write_results(output_file, results)
        print(f"Результаты записаны в {output_file}")
        logging.info("Скрипт завершил выполнение.")
