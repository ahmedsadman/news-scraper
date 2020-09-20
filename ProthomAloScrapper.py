import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.prothomalo.com/search")

stories_container = driver.find_element_by_class_name(
    "searchStories1AdWithLoadMore-m__stories__2SFip"
)

story_cards = stories_container.find_elements_by_class_name(
    "customStoryCard9-m__wrapper__yEFJV"
)
load_more_button = driver.find_element_by_class_name("more-m__bn-content__3Ppnx")

links = [
    card.find_element_by_tag_name("a").get_attribute("href") for card in story_cards
]


for link in links:
    driver.get(link)
    time.sleep(3)
    heading = driver.find_element_by_tag_name("h1")
    print(heading.text)
    p = driver.find_elements_by_tag_name("p")
    for _p in p:
        print(_p.text)
    print("---------------")

# print("Waiting..")
# time.sleep(5)
# load_more_button.click()
# print("Clicked")

# driver.close()
