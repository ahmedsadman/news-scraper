# News Scraper

A scrapper to scrape popular news websites of Bangladesh. This is intended to be used as a tool to create data corpus for Bengali language.

## Usage

Python 3.6+ is required. Install the libraries using. Create a virtualenv if required and then install the requirments

```
pip install -r requirements.txt
```

### Prothom Alo Scrapper

`ProthomAloScrapper.batch_scrape(total_iterations)` - scrapes data from the corresponding website. Here `total_iterations` refers to the no of times 'Load More' button should be clicked. Each click adds 6 news to the list. Initially there are ten 10 loaded.

So if `total_iterations=20` then the expected number of news to be scraped is `10 + 20 * 6 = 130`. The final number might be less than expected because some articles will be discarded due to not meeting scraping criteria (like video-only type posts).
