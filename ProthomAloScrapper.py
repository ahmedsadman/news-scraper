import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProthomAloScrapper:
    def __init__(self):
        self.BASE_URL = "https://www.prothomalo.com/search"
        self.driver = webdriver.Chrome()
        self.news_links = []

    def get_news_links(self):
        if self.news_links:
            return self.news_links

        self.driver.get(self.BASE_URL)
        stories_container = self.driver.find_element_by_class_name(
            "searchStories1AdWithLoadMore-m__stories__2SFip"
        )
        story_cards = stories_container.find_elements_by_class_name(
            "customStoryCard9-m__wrapper__yEFJV"
        )
        self.news_links = [
            card.find_element_by_tag_name("a").get_attribute("href")
            for card in story_cards
        ]

        return self.news_links

    def scrape_article(self, url, wait_time=5):
        self.driver.get(url)
        # time.sleep(wait_time)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )
        heading = self.driver.find_element_by_tag_name("h1")
        print(heading.text)

        paras = self.driver.find_elements_by_tag_name("p")
        paras = [para.text for para in paras]
        for para in paras:
            print(para)
        print("---------------")

    def batch_scrape(self):
        self.get_news_links()
        for link in self.news_links:
            self.scrape_article(link)

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    pa_scrapper = ProthomAloScrapper()
    pa_scrapper.batch_scrape()