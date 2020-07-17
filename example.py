
from Scraper import GlassdoorJobScraper
from selenium import webdriver
path = "C:\chromedriver.exe"

js = GlassdoorJobScraper(path, chrome=True, driver_options= webdriver.ChromeOptions())
data = js.scrape(["Machine Learning Engineer", "Data Scientist", "Software Engineer"], jobs_num=900)
data.to_csv("./jobs_clean.csv", header=True, index=False)