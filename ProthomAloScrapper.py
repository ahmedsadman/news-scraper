import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.prothomalo.com/search")

stories_container = driver.find_element_by_class_name(
    "searchStories1AdWithLoadMore-m__stories__2SFip"
)

links = stories_container.find_elements_by_tag_name("a")
load_more_button = driver.find_element_by_class_name("more-m__bn-content__3Ppnx")

for link in links:
    print(link.get_attribute("href"))

print("Waiting..")
time.sleep(5)
load_more_button.click()
print("Clicked")

print("Waiting..")
time.sleep(5)
load_more_button.click()
print("Clicked")
# driver.close()
