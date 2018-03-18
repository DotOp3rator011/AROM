import logging
from .Scraper import Scraper
import json


def save_to_json(reviews):
    """ Save the reviews to Corpus.json file
    Args:
        reviews (list): list of all the scraped reviews
    returns:
        None
    """

    with open("Corpus.json", "a") as jf:
        json.dump(reviews, jf, sort_keys=True, indent=4)


def compile_reviews(review_text, review_stars):
    """ Complie a dictionary of the review's text, review's stars and lable the
        review as poitive or negative
    Args:
        review_text (list): text of the reviews
        review_stars (list): star rating of the reviews
    Returns:
        reviews (list): list of all the complied reviews
    """

    reviews = list()
    global neg_count
    global pos_count
    for t, s in zip(review_text, review_stars):
        review_dict = dict()
        review_dict["text"] = t.text.encode("ascii", "ignore").decode()
        review_dict["stars"] = int(s.text.encode("ascii", "ignore").decode()[0])
        if review_dict["stars"] <= 2:
            review_dict["label"] = "negative"
            neg_count += 1
            if neg_count <= 50:
                reviews.append(review_dict)
        elif review_dict["stars"] >= 4:
            review_dict["label"] = "positive"
            pos_count += 1
            if pos_count <= 50:
                reviews.append(review_dict)
        else:
            continue
    return reviews


def get_reviews(url):
    """ Scrape reviews off each review page
    Args:
        url (str): url of the product page
    Returns:
        reviews (list): list of all the scraped reviews
    """

    scraper = Scraper()
    review_url = scraper.get_reviews_page(url)
    soup = scraper.get_soup(review_url)
    lastPage = scraper.get_last_page(soup)
    reviews = list()
    global neg_count
    global pos_count
    for i in range(1, lastPage + 1):
        if neg_count >= 50 and pos_count >= 50:
            return reviews
        soup = scraper.get_soup(review_url + "&pageNumber=" + str(i))
        review_stars = soup.find_all(attrs={"data-hook": "review-star-rating"})
        review_text = soup.find_all("span", 'a-size-base review-text')
        reviews += compile_reviews(review_text, review_stars)
    return reviews


def get_asin_list():
    """ Read asin form AsinList.txt
    Args:
        None
    Returns:
        asinList (list): returns a list of asin from AsinList.txt
    """

    with open("AsinList.txt", "r") as alf:
        content = alf.read()
        asinList = content.split()
        return asinList


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asinList = get_asin_list()
    reviews = list()
    prevLen = 0
    for asin in asinList:
        try:
            url = "https://www.amazon.in/dp/" + asin
            neg_count = 0
            pos_count = 0
            reviews += get_reviews(url)
            logging.info(asin + " -- " + str(len(reviews) - prevLen) + "\n")
            prevLen = len(reviews)
        except Exception as e:
            logging.info(asin + " -- " + str(e) + "\n")
            asinList.append(asin)
    save_to_json(reviews)
