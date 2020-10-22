import sys
import requests
import time
import re
import csv
from datetime import datetime


class ProthomAloApi:
    def __init__(self, output_file="output.csv"):
        self.items = []
        self.output_file = output_file
        self.script_start = None
        self.script_end = None
        self.ids = set()

    def process_article_data(self, data):
        """
        Extract the headline, main content and tags of articles and store in
        items array
        """
        processed_articles = []  # tuples -> (headline, content, tags)

        for article in data:
            if article["id"] in self.ids:
                continue
            headline = article["headline"]
            tags = self.extract_tags(article["tags"])
            content = self.process_content(article["cards"])

            if content is not None:
                # ignore empty content news
                processed_articles.append((headline, content, tags))
                self.ids.add(article["id"])

        self.items += processed_articles  # concat array

    def convert_to_unixtime(self, datestr):
        date = datetime.strptime(datestr, "%d-%m-%Y")
        return int(date.timestamp() * 1000)  # convert to milliseconds

    def extract_tags(self, tag_data):
        tags = []
        for item in tag_data:
            tags.append(item["name"])
        return ",".join(tags)

    def process_content(self, cards):
        content = []
        for items in cards:
            for element in items["story-elements"]:
                if element["type"] == "text":
                    text = self.strip_html(element["text"])
                    content.append(text)
        return "".join(content) if len(content) > 0 else None

    def strip_html(self, text):
        """Remove all HTML tags from given text"""
        cleanr = re.compile("<.*?>|&.*;")
        cleantext = re.sub(cleanr, "", text)
        return cleantext

    def fetch(self, start_time, end_time, offset=0, limit=100):
        """
        Method to fetch news data from ProthomAlo advanced search API
        start_time (int) -> unix epoch in milliseconds
        end_time (int) -> unix epoch in milliseconds
        offset (int) -> number of news to skip
        """
        total = None
        while total is None or total > 0:
            print(f"Processing Offset: {offset}, Limit: {limit}")
            request_url = (
                f"https://www.prothomalo.com/api/v1/advanced-search?"
                + f"fields=headline,tags,cards&offset={offset}&limit={limit}"
                + f"&sort=latest-published&published-after={start_time}&published-before={end_time}"
            )
            response = requests.get(request_url)
            response = response.json()

            if total is None:
                total = response["total"]
            if len(response["items"]) == 0:
                break

            self.process_article_data(response["items"])
            offset += limit
            total -= len(response["items"])

    def write_output(self):
        with open(self.output_file, "w", encoding="utf-8", newline="\n") as f:
            csv_writer = csv.writer(f, delimiter=",")
            csv_writer.writerow(("title", "content", "tags"))
            for item in self.items:
                csv_writer.writerow(item)

    def show_stat(self):
        print(f"Total Article: {len(self.items)}")

    def scrape_articles(self, start_time, end_time):
        start_time = api.convert_to_unixtime(start_time)
        end_time = api.convert_to_unixtime(end_time)
        api.fetch(start_time, end_time)
        api.write_output()
        api.show_stat()


if __name__ == "__main__":
    api = ProthomAloApi(sys.argv[1])
    api.scrape_articles(sys.argv[2], sys.argv[3])
    # print(api.convert_to_unixtime("7-6-2012"))
    # print(api.convert_to_unixtime("30-6-2012"))
