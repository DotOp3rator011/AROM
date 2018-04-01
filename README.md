# AROM

To extract product reviews, from amazon.com and classifying the reviews as positive or negative. Implementing web
scraping technologies, to extract reviews of the user desired product, from amazon.com. Implementing a statistical
supervised learning model, to perform sentiment analysis and classify the reviews as bearing positive or negative
polarity. Collecting user input and graphical representation of the data from the analysis in a web-based user
interface.

# User Interface
The user interface is designed using web technologies like HTML5, CSS3, Bootstrap4, and JavaScript. The user interface
facilitates the user to input an ASIN of any product, whose reviews are to be classified as bearing positive or negative
polarity from amazon.com. Amazon Standard Identification Numbers (ASINs) are unique blocks of 10 letters and/or numbers
that identify items. You can find the ASIN on the item's product information page at Amazon.com. For books, the ASIN is
the same as the ISBN number, but for all other products, a new ASIN is created when the item is uploaded to Amazon’s
catalog. The Python / Django Framework connects the user interface with the backend. The analysis of the reviews
classification is visualized on the user interface through a doughnut chart, which depicts the ratio of the percentage
of positive reviews to the percentage of negative reviews. The user interface also facilitates a user feedback or
request section, and a brief description of the project.

# Scraper
The scraper module is built in Python 3.6, utilizing Python’s and Web Scraping libraries, Selenium and Beautiful Soup.
Web scraping is a process of data extraction from websites. All the job is carried out by a piece of code which is
called a “scraper”. First, it sends a “GET” query to a specific website. Then, it parses the HTML document based on the
received result. After it’s done, the scraper searches for the data within the document, and, finally, convert it into a
specified format. The ASIN inputted from the user is used to compute the product link to extract reviews from on the
amazon.com website. The Selenium Web Driver is used to navigate to the reviews section of the product page. The BS4
library is used to convert the HTML content of the reviews page into a python object tree called “Soup”. The tree can be
navigated using a Soup Object. The soup object is used to extract the review text and the reviews are stored as a list
of strings.

# Sentiment Classifier
The Sentiment Classifier module is built in Python 3.6, utilizing Python’s Natural Language Processing library, Natural
Language Toolkit (NLTK). The list of reviews, obtained from the scraper module are passed iteratively to the Naive Bayes
Classifier, to be classified a reviews bearing positive or negative polarity. The Naive Bayes Classifier is trained
using training data, extracted from a corpus. The corpus consists of 1500 positive reviews and 1500 negative reviews,
extracted from various Amazon products. The reviews extracted are classified as positive or negative reviews, based on
the star ratings. The reviews bearing 4 or 5 stars are classified as positive and the reviews bearing the 1 or 2 stars
are classified as negative. The reviews bearing 3 stars are omitted due to ambiguity. Once the reviews of the user
desired product are classified, the percentage of positive reviews and the percentage of negative reviews are computed.
The analysis is visualized to the user, through a doughnut chart on the user interface.



