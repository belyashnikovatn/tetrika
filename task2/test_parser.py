import unittest
from unittest.mock import AsyncMock, patch
import asyncio
from collections import defaultdict

from task2.solution import process_page, get_all_page_links, BASE_URL

HTML_PAGE = """
<html>
<body>
<div class="mw-category">
  <div class="mw-category-group">
    <ul>
      <li><a href="/wiki/Акула">Акула</a></li>
      <li><a href="/wiki/Бобр">Бобр</a></li>
    </ul>
  </div>
</div>
<a href="/wiki/Категория:Животные_по_алфавиту?pagefrom=Бобр" title="Следующая страница">Следующая страница</a>
</body>
</html>
"""

HTML_LAST_PAGE = """
<html>
<body>
<div class="mw-category">
  <div class="mw-category-group">
    <ul>
      <li><a href="/wiki/Волк">Волк</a></li>
    </ul>
  </div>
</div>
</body>
</html>
"""


class TestWikiAnimalParser(unittest.IsolatedAsyncioTestCase):

    @patch("task2.solution.fetch", new_callable=AsyncMock)
    async def test_get_all_page_links(self, mock_fetch):
        mock_fetch.side_effect = [HTML_PAGE, HTML_LAST_PAGE]

        links = await get_all_page_links(
            BASE_URL + "/wiki/Категория:Животные_по_алфавиту"
        )
        self.assertEqual(len(links), 2)
        self.assertTrue(links[0].endswith("_по_алфавиту"))
        self.assertIn("pagefrom=Бобр", links[1])

    @patch("task2.solution.fetch", new_callable=AsyncMock)
    async def test_process_page(self, mock_fetch):
        mock_fetch.return_value = HTML_PAGE

        letter_counts = defaultdict(int)
        semaphore = asyncio.Semaphore(1)

        async with asyncio.Semaphore(1):
            await process_page(
                None,
                "http://example.com",
                letter_counts,
                semaphore,
            )

        self.assertEqual(letter_counts["А"], 1)
        self.assertEqual(letter_counts["Б"], 1)


if __name__ == "__main__":
    unittest.main()
