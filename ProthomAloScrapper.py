import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class ProthomAloScrapper:
    def __init__(self):
        self.BASE_URL = "https://www.prothomalo.com/search"
        self.driver = webdriver.Chrome()
        self.news_links = []
        self.csv_file = open("output.csv", "w", encoding="utf-8", newline="\n")
        self.csv_writer = csv.writer(self.csv_file, delimiter=",")
        self.csv_writer.writerow(["title", "content", "tags"])

        self.total_scraped = 0
        self.total_errors = 0

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
            print("Ad banner removed...")
            print("Continuing...")
            return True
        except Exception as e:
            pass

    def load_more(self, total_iterations=10):
        """
        Click the load more button to load more news in the list. At this moment,
        there are 10 inital news in the list, and 5 more are added each time load button
        is clicked. The 'iterations' refer to no of times to click the load button.
        """
        ad_banner_removed = False
        load_button = self.driver.find_element_by_class_name("more-m__wrapper__2sxTa")
        temp_iter = total_iterations

        try:
            while temp_iter > 0:
                self.scroll_to_element(self.driver, load_button)
                if not ad_banner_removed:
                    print("Trying to remove ad banner...")
                    time.sleep(3)
                    ad_banner_removed = self.remove_ad_banner()

                load_button.click()
                temp_iter -= 1
                print(f"Iteration {total_iterations - temp_iter}/{total_iterations}")
                time.sleep(2)
        except StaleElementReferenceException as e:
            print("Reached end of news for the given timeframe")

    def get_news_links(self, total_iterations=10):
        if self.news_links:
            return self.news_links

        self.driver.get(self.BASE_URL)

        print("You can set date range filters now.")
        print("Watiting for user preparation. Press ENTER to continue")
        input("")

        # load all links before starting to process
        print("Getting news article links...")
        self.load_more(total_iterations)

        stories_container = self.driver.find_element_by_class_name(
            "searchStories1AdWithLoadMore-m__stories__2SFip"
        )
        story_cards = stories_container.find_elements_by_class_name(
            "customStoryCard9-m__wrapper__yEFJV"
        )

        # populate links. Set is used to avoid duplicates
        links = set()
        for card in story_cards:
            url = card.find_element_by_tag_name("a").get_attribute("href")
            links.add(url)

        self.news_links = list(links)
        return self.news_links

    def scrape_article(self, browser, url):
        try:
            # avoid only-video type articles
            if "video/" in url:
                return

            print(f"Scraping url: {url}")
            browser.get(url)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )

            heading = browser.find_element_by_tag_name("h1").text.strip()
            paras = browser.find_elements_by_tag_name("p")
            paras = [para.text.replace("\n", "").replace("\r", "") for para in paras]
            paras = " ".join(paras)

            # get the tags
            tags = browser.find_elements_by_class_name("storyTag-m__story-tag__uEX9i")
            tags = [tag.text.strip() for tag in tags]
            tags = ",".join(tags)

            # write output to csv
            self.csv_writer.writerow([heading, paras, tags])

            self.total_scraped += 1

        except Exception as e:
            print(
                f"Error occured for while scraping URL: {url}. Either scrape requirements were invalid or IO error occured"
            )
            self.total_errors += 1

    def batch_scrape(self, total_iterations=10):
        """
        Batch scrape news articles
        Iterations = number of times 'load more' button to click
        Initially there are 10 articles. One iteration adds 6 news articles/
        So iteration = 20 should produce 10 + 20 * 6 = 130 articles

        Please note that final output might not have 130 articles because
        some might get discarded due to errors or being video-only articles
        """
        self.total_errors = 0
        self.total_scraped = 0
        start_time = time.time()

        print("Starting batch scraping...")
        self.get_news_links(total_iterations)
        for link in self.news_links:
            self.scrape_article(self.driver, link)

        end_time = time.time()
        print(" -- COMPLETE --")
        print(f"Time required: {end_time - start_time} sec")
        print(f"Total Scraped Articles: {self.total_scraped}")
        print(f"Total Errors: {self.total_errors}")

    def __del__(self):
        self.driver.close()
        self.csv_file.close()


if __name__ == "__main__":
    pa_scrapper = ProthomAloScrapper()
    pa_scrapper.batch_scrape(total_iterations=200)