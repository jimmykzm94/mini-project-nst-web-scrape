# Mini project - NST web scrape

## Description
This project demonstrates how to scrape articles from the NST website using Selenium web driver and Beautifulsoup. It covers fetching web pages, parsing HTML content, and extracting relevant information.

## Demo
Each command below runs the scraper in a different mode:

- `python nst_news.py --mode highlights`  
    Scrapes the top highlighted news articles.

- `python nst_news.py --mode latest`  
    Scrapes the most recent news articles.

- `python nst_news.py --mode worlds`  
    Scrapes news articles from the "Worlds" section.

- `python nst_news.py --mode search --query "education" --limit 10`  
    Searches for articles containing the keyword "education" and returns up to 10 results.

## Keywords
![Python](https://img.shields.io/badge/Language-Python-blue)
![WebScraping](https://img.shields.io/badge/-WebScraping-red)