import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

class Parser:
    def __init__(self):
        self.base_url = "https://downdetector.su/"
        self.results = []

    async def parse_branch(self, branch):
        url = f"{self.base_url}branches/{branch}"
        try:
            with requests.Session() as sess:
                resp = sess.get(url, headers=header, timeout=(4, 27))
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')

            cards_down = soup.find_all("a", class_="card down")

            for card in cards_down:
                span_elements = card.find_all("span")
                for span in span_elements:
                    self.results.append(span.text)

        except requests.RequestException as e:
            print(f"An error occurred while fetching the page for branch '{branch}': {e}")

    async def parse(self, branches):
        for branch in branches:
            await self.parse_branch(branch)
        return self.results
