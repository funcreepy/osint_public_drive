import logging
import requests
import time
import random

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def generate_random_headers():
    """Генерация случайных заголовков."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.4600.100 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.3945.88 Safari/537.36"
    ]
    platforms = ["\"macOS\"", "\"Windows\"", "\"Linux\""]
    sec_ch_ua = random.choice([
        "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "\"Google Chrome\";v=\"130\", \"Chromium\";v=\"130\"",
        "\"Microsoft Edge\";v=\"112\", \"Chromium\";v=\"112\""
    ])

    return {
        "Sec-Ch-Ua": sec_ch_ua,
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": random.choice(platforms),
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }

def check_url(url, cookies=""):
    """Функция для проверки URL."""
    try:
        headers = generate_random_headers()
        response = requests.get(url, timeout=5, allow_redirects=True, cookies={"Cookie": cookies}, headers=headers)
        if response.status_code == 200 and response.url != url:
            logging.warning(f"Redirect detected for {url} -> {response.url}. Treating as 403.")
            return url, 403
        return url, response.status_code
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе к {url}: {e}")
        return url, None

def process_urls(file_input, file_output, cookies=""):
    """Функция для обработки списка URL."""
    with open(file_input, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []
    for url in urls:
        url, status_code = check_url(url, cookies)
        results.append((url, status_code))
        logging.info(f"{url} - {status_code}")
        time.sleep(random.uniform(3, 7))  # Рандомная задержка между 1 и 3 секундами

    with open(file_output, "w") as f:
        for url, status_code in results:	
            f.write(f"{url} - {status_code}\n")

if __name__ == "__main__":
    input_file = "jira_links_url.txt"  # Входной файл с URL
    output_file = "results.txt"  # Выходной файл с результатами
    cookies = ""  # Строка cookies
    process_urls(input_file, output_file, cookies=cookies)
