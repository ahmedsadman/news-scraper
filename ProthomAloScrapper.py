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

    def scroll_to_element(self, browser, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def remove_ad_banner(self):
        # remove the ad banner if it pops up, otherwise it would cause click issues
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (
                        By.CLASS_NAME,
                        "breakingNewsSlider-m__ad-close__2GnO5",
                    )
                )
            )
            ad_banner_close = self.driver.find_element_by_class_name(
                "breakingNewsSlider-m__ad-close__2GnO5"
            )
            self.scroll_to_element(self.driver, ad_banner_close)
            ad_banner_close.click()
            time.sleep(3)
            return True
        except Exception as e:
            pass

    def load_more(self, iterations=10):
        """
        Click the load more button to load more news in the list. At this moment,
        there are 10 inital news in the list, and 5 more are added each time load button
        is clicked. The 'iterations' refer to no of times to click the load button.
        """
        ad_banner_removed = False
        while iterations > 0:
            print("waiting...")
            load_button = self.driver.find_element_by_class_name(
                "more-m__wrapper__2sxTa"
            )
            self.scroll_to_element(self.driver, load_button)

            if not ad_banner_removed:
                print("trying to remove ad banner")
                time.sleep(3)
                ad_banner_removed = self.remove_ad_banner()

            load_button.click()
            print("clicked")
            iterations -= 1
            time.sleep(3)

    def get_news_links(self):
        if self.news_links:
            return self.news_links

        self.driver.get(self.BASE_URL)

        # load all links before starting to process
        self.load_more(5)

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

    def scrape_article(self, browser, url, wait_time=5):
        try:
            browser.get(url)
            # time.sleep(wait_time)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )
            heading = browser.find_element_by_tag_name("h1")
            print(heading.text)

            paras = browser.find_elements_by_tag_name("p")
            paras = [para.text for para in paras]
            for para in paras:
                print(para)
            print("---------------")
        except Exception as e:
            pass

    def batch_scrape(self):
        self.get_news_links()
        for link in self.news_links:
            self.scrape_article(self.driver, link)

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    pa_scrapper = ProthomAloScrapper()
    pa_scrapper.batch_scrape()