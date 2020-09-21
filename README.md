# News Scraper

A scrapper to scrape popular news websites of Bangladesh. This is intended to be used as a tool to create data corpus for Bengali language.

## Usage

-   Python 3.6+ is required. Install the libraries using. Create a virtualenv if required and then install the requirments

```
pip install -r requirements.txt
```

-   The scraper uses ChromeDriver. The driver has to match exactly with your current Chrome version. [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in the root folder.

### Prothom Alo Scrapper

`ProthomAloScrapper.batch_scrape(total_iterations)` - scrapes data from the corresponding website. Here `total_iterations` refers to the no of times 'Load More' button should be clicked. Each click adds 6 news to the list. Initially there are ten 10 loaded.

So if `total_iterations=20` then the expected number of news to be scraped is `10 + 20 * 6 = 130`. The final number might be less than expected because some articles will be discarded due to not meeting scraping criteria (like video-only type posts).

_Currently Prothom Alo website has a limitation where news is repeated after loading 5-6 days news
on the same page. So users are requested to set a filter on date range of 5-6 days and do scraping in chunks. For this, you will get time to set the filter before scraping starts. Later, automation
will be added for this. For 5-6 days range, `total_iterations=200` would be an ideal value. When news comes to an end for the given timerange, the iteration will stop automatically. So you should set `total_iterations` as high as possible to get all the news for the given range_
