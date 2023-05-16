# Investigating the differences between Darknet, deepweb and surfaceweb forums

Motivation: Scraping darknet forums has been the object of research in the field of intelligence and security informatics (Fu et al., 2010), (Ding et al., 2021).
In this repository we scraped three different sources of forums, and performed the following analysis:
- Sentiment Analysis
- Topic Modelling: a good approach in understanding the content of darknet forums (Nazah et al. 2021)
- Linguistic Analysis: Vocabulary, word count and emphasis (by the usage of uppercase) are possible extracted features that could differ between domains (Du et al., 2019)

# Folder structure
- scraper
Notebooks for scraping the following forums:
    - Dark Web Scraper (8chan)
    - Hidden Surface Web Page Scraper (8kun)
    - Surface Web Page Scraper (VGR)

- data
Datasets in csv format and a cleaned parquet for pandas DataFrame.
  - Dark Web Data Set (8chan)
  - Hidden Surface Web Page Data Set (8kun)
  - Surface Web Page Data Set (VGR)

- output
Every analysed forum has:
  - [source]_analysis.parquet: Sentiment Analysis
  - [source]_dictionary: Most common words and ngrams used in the forum
  - [source]_ldavis_[n]: A visualisation of the topic modelling from the LDA and [n] topics

- utils
Module with auxiliary functions.

# Scrapers and Extractors
In this repository, there is code for three different scrapers and one extractor 
that has been run separately from the scraping.

## Which forums have been scraped and how?
For comparison, a single common topic was chosen between all forums. Thus, the videogames section has been scraped. 

### The Dark Web
On the dark web, 8chan (/v) has been scraped. The TOR client has to be installed and 
activated on the user's machine, after which the scraper can be run. Note that the
TOR client needs to run on default settings (port 9050).

A session will be created by using the requests library to run the scraper. 
The cookie is provided to bypass the captcha on the website. This cookie might have 
to be renewed if re-scraping this website.

The obtained data is saved in a text file, which can be run in the extractor to obtain the 
relevant information from the web pages and create a DataFrame (and `csv` file) with all
information. The extractor uses BeautifulSoup to obtain the relevant information.

### The Hidden Surface Web
Some webpages can be found on the surface web, but are not indexed by Google and other
search engines, making them more hidden compared to normal websites. We have decided to
scrape 8kun (/v), the surface web alternative of 8chan after 8chan was shut down on the 
surface web.

The normal requests library is used to scrape the data and the data is obtained via 
BeautifulSoup. It is saved to a `csv` file.

### The Surface Web
As a comparison, VGR.com has been scraped on the surface web. From this video gaming website,
only the `Gaming Forum` has been scraped. This is done since most conversations on the 
Dark Web forum and the hidden surface web forum on /v where (meant to be) on the games 
itself as well and not the machines on which the games are run.

Since the surface web has more content compared to the Dark Web and hidden surface web forums 
we have found, only the first page of each thread has been scraped instead of all pages.

The normal requests library is used to scrape the data and the data is obtained via
BeautifulSoup. It is saved to a `csv` file.

# Results
The [moderation API from OpenAi](https://platform.openai.com/docs/guides/moderation) was not very effective in this studied case. Two different approaches were tested: post per post analysis and for a whole topic. No content was flagged any of the moderated categories: "hate", "hate/threatening", "self-harm", "sexual", "sexual/minors", "violence", "violence/graphic". Scores were very similarly low across the whole dataset. The documentation of the API explicits that it looks for "hateful, harassing, or violent content that:
- expresses, incites, or promotes hate based on identity
- intends to harass, threaten, or bully an individual
- promotes or glorifies violence or celebrates the suffering or humiliation of others

A hypothesis is that the API only flags things that are extremes in their categories. In special the highest score for hate, albeit barely higher than other samples, was for the post "Remember to keep killing <group of people, redacted>. They are afraid, and they know that they don't have any future.". The example does indeed show hate, but even the second in this category and other categories do not present high scores according to the API.

# References
Fu, T., Abbasi, A. and Chen, H. (2010), "A focused crawler for Dark Web forums". J. Am. Soc. Inf. Sci., 61: 1213-1231. https://doi.org/10.1002/asi.21323

S. Nazah, S. Huda, J. H. Abawajy and M. M. Hassan (2021), "An Unsupervised Model for Identifying and Characterizing Dark Web Forums," in IEEE Access, vol. 9, pp. 112871-112892, doi: 10.1109/ACCESS.2021.3103319.

P. -Y. Du, M. Ebrahimi, N. Zhang, H. Chen, R. A. Brown and S. Samtani, (2019) "Identifying High-Impact Opioid Products and Key Sellers in Dark Net Marketplaces: An Interpretable Text Analytics Approach,"  IEEE International Conference on Intelligence and Security Informatics (ISI), Shenzhen, China, 2019, pp. 110-115, doi: 10.1109/ISI.2019.8823196.

Z. Ding, V. Benjamin, W. Li and X. Yin, (2021) "Exploring Differences Among Darknet and Surface Internet Hacking Communities," 2021 IEEE International Conference on Intelligence and Security Informatics (ISI), San Antonio, TX, USA, pp. 1-3, doi: 10.1109/ISI53945.2021.9624681.
