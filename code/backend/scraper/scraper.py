"""
Selenium script to extract data from pages
"""


from bs4 import BeautifulSoup

# -*- coding: utf-8 -*-
from dateutil import parser
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def extract_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="Tap to show more book description"]')
            )
        ).click()
    except (
        NoSuchElementException,
        ElementNotInteractableException,
        TimeoutException,
        ElementClickInterceptedException,
    ):
        print("Button to expand summary not found on this page: " + url)

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="Book details and editions"]')
            )
        ).click()
    except (
        NoSuchElementException,
        ElementNotInteractableException,
        TimeoutException,
        ElementClickInterceptedException,
    ):
        print("Button to expand book details not found on this page: " + url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = ""
    author = ""
    rating = 0.0
    summary = ""
    genres = []
    number_of_pages = 0
    release_date = ""
    isbn = ""
    language = ""

    title = soup.find("h1", {"class": "Text__title1"}).text
    author = soup.find("span", {"class": "ContributorLink__name"}).text

    try:
        rating = float(soup.find("div", {"class": "RatingStatistics__rating"}).text)
    except ValueError:
        print("Cannot retrieve book rating")

    summary = soup.find(
        "div", {"class": "DetailsLayoutRightParagraph__widthConstrained"}
    ).text.replace("\n", " ")
    cover_page = soup.find("img", {"class": "ResponsiveImage"}).get("src")

    for genre in soup.find_all(
        "span", {"class": "BookPageMetadataSection__genreButton"}
    ):
        genres.append(genre.find("span", {"class": "Button__labelItem"}).text)

    for item in soup.find_all("div", {"class": "DescListItem"})[-4:]:
        selector = item.find("dt").text
        if selector == "Format":
            try:
                number_of_pages = int(
                    (
                        item.find("div", {"class": "TruncatedContent"})
                        .find("div", {"data-testid": "contentContainer"})
                        .text.split(",")[0]
                        .split(" ")[0]
                    )
                )
            except ValueError:
                print("Cannot retrieve page number")
        elif selector == "Published":
            try:
                release_date = parser.parse(
                    " ".join(
                        item.find("div", {"class": "TruncatedContent"})
                        .find("div", {"data-testid": "contentContainer"})
                        .text.split(" ")[:3]
                    )
                )
            except ValueError:
                print("Cannot retrieve release date")
        elif selector == "ISBN":
            isbn = (
                item.find("div", {"class": "TruncatedContent"})
                .find("div", {"data-testid": "contentContainer"})
                .text.split(" ")[0]
            )
        elif selector == "Language":
            language = (
                item.find("div", {"class": "TruncatedContent"})
                .find("div", {"data-testid": "contentContainer"})
                .text
            )
        else:
            continue

    driver.quit()
    return [
        title,
        author,
        rating,
        summary,
        cover_page,
        genres,
        number_of_pages,
        release_date,
        isbn,
        language,
    ]
