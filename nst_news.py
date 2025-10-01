from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class NSTArticle:
    def __init__(self):
        self.url = "https://www.nst.com.my"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_options.add_argument("--disable-gpu")     # safer for headless
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")  # disable popup dialogs
        chrome_options.add_argument("--disable-notifications")   # disable notification prompts
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # disable images

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(15)
        # self.driver.execute_cdp_cmd(
        #     "Page.addScriptToEvaluateOnNewDocument",
        #     {"source": "setTimeout(() => window.stop(), 1000);"}
        # )

    def close(self):
        self.driver.quit()

    def scrape_index(self):
        messages = []
        try:
            self.driver.get(self.url)

            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            section_highlight = soup.find('div', class_='section-highlights')

            for a in section_highlight.find_all('a')[:13]: # top highlight and 12 hightlights
                url = a.get("href")
                title_tag = a.select_one("h2.teaser-title").get_text()
                time_tag = a.select_one("div.text-gray-400").get_text()

                messages.append(f"Title: {title_tag} | Time: {time_tag} | URL: {url}")
        except Exception as e:
            print(f"Error occurred: {e}")
        return messages

    def scrape_latest(self):
        messages = []
        try:
            self.driver.get(self.url)

            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # select only real slides, skip clones
            latest_section = soup.find('div', class_='carousel-title')
            slides = latest_section.select("ul.splide__list li.splide__slide:not(.splide__slide--clone)")

            for slide in slides:
                url = slide.select_one("a.teaser-title").get("href")
                title = slide.select_one("a.teaser-title").get_text(strip=True)
                time = slide.select_one("div.text-gray-400").get_text(strip=True)
                messages.append(f"Title: {title} | Time: {time} ago | URL: {url}")
        except Exception as e:
            print(f"Error occurred: {e}")
        return messages

    def scrape_worlds(self):
        messages = []
        try:
            url = f"{self.url}/world/world"
            self.driver.get(url)
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            world_section = soup.find('div', class_='category-listing')

            if world_section:
                for a in world_section.find_all('a'):
                    url = a.get("href")
                    title_tag = a.select_one("h2.teaser-title").get_text()
                    time_tag = a.select_one("div.text-gray-400").get_text()
                    messages.append(f"Title: {title_tag} | Time: {time_tag} | URL: {url}")
            else:
                print("Could not find the main 'World' section container.")
        except Exception as e:
            print(f"Error occurred: {e}")
        return messages

    def scrape_search_results(self, query, limit=5):
        messages = []
        try:
            # space in query should be replaced with %20
            query = query.replace(' ', '%20')
            url = f"{self.url}/search?keywords={query}"
            self.driver.get(url)
            html_content = self.driver.page_source

            # type, time, title, url
            if html_content:
                # Find the articles
                soup = BeautifulSoup(html_content, 'html.parser')
                search_section = soup.find('div', class_='search-results')
                if search_section:
                    for a in search_section.find_all("a")[:limit]:
                        url = a.get("href")
                        title_tag = a.select_one("h2.teaser-title").get_text()
                        time_tag = a.select_one("div.text-gray-400").get_text()
                        messages.append(f"Title: {title_tag} | Time: {time_tag} | URL: {url}")
        except Exception as e:
            print(f"Error occurred: {e}")
        return messages

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="NST News Scraper")
    parser.add_argument('--mode', type=str, choices=['highlights', 'latest', 'worlds', 'search'], default='highlights', help='Scraping mode')
    parser.add_argument('--query', type=str, help='Search query (required if mode is search)')
    parser.add_argument('--limit', type=int, default=5, help='Number of search results to return (only for search mode)')
    args = parser.parse_args()

    nst = NSTArticle()
    exit_code = 0
    results = []

    if args.mode == 'highlights':
        results = nst.scrape_index()
    elif args.mode == 'latest':
        results = nst.scrape_latest()
    elif args.mode == 'worlds':
        results = nst.scrape_worlds()
    elif args.mode == 'search':
        if not args.query:
            print("Error: --query is required for search mode")
            exit_code = 1
        results = nst.scrape_search_results(args.query, limit=args.limit)
    else:
        print("Invalid mode selected.")
        exit_code = 1
    nst.close()

    # Print results
    for message in results:
        print(message)
    
    # Exit okay
    sys.exit(exit_code)
