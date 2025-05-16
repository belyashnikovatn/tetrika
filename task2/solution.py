import asyncio
import aiohttp
from bs4 import BeautifulSoup
from collections import defaultdict
import csv
from tqdm import tqdm

BASE_URL = "https://ru.wikipedia.org"
START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AsyncBot/1.0)"}

CONCURRENT_REQUESTS = 5  # ограничиваем количество одновременных запросов


async def fetch(session, url, semaphore):
    async with semaphore:
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()


async def get_all_page_links(start_url):
    """
    Возвращает список всех URL со страницами животных.
    """
    urls = [start_url]
    async with aiohttp.ClientSession() as session:
        while True:
            html = await fetch(session, urls[-1], asyncio.Semaphore(1))
            soup = BeautifulSoup(html, "html.parser")
            next_link = soup.find("a", string="Следующая страница")
            if next_link:
                next_url = BASE_URL + next_link["href"]
                if next_url in urls:
                    break
                urls.append(next_url)
            else:
                break
    return urls


async def process_page(session, url, letter_counts, semaphore):
    html = await fetch(session, url, semaphore)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.mw-category div.mw-category-group ul li")
    for item in items:
        title = item.text.strip()
        if title:
            first_letter = title[0].upper()
            letter_counts[first_letter] += 1


async def main():
    letter_counts = defaultdict(int)
    urls = await get_all_page_links(START_URL)

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(process_page(session, url, letter_counts, semaphore))

        for f in tqdm(
            asyncio.as_completed(tasks), total=len(tasks), desc="Обработка"
        ):
            await f

    # Сохраняем в CSV
    with open("beasts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for letter in sorted(letter_counts):
            writer.writerow([letter, letter_counts[letter]])

    print("Готово! Файл beasts.csv создан.")


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
