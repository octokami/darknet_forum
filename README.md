# Investigating the differences between Darknet, deepweb and surfaceweb forums

Motivation: Scraping darknet forums has been the object of research in the field of intelligence and security informatics (Fu et al., 2010), (Ding et al., 2021).
In this repository we scraped three different sources of forums, and performed the following analysis:
- Sentiment Analysis: In combination with Named Entity Recognition (NER) could be an actionable tool for threat intelligence (Evangelatos et al. 2021), (El Barachi, 2022).
- Topic Modelling: a good approach in understanding the content of darknet forums (Nazah et al. 2021). Technique used: Latent Dirichlet Allocation (LDA). 
- Linguistic Analysis: vocabulary, word count and emphasis (by the usage of uppercase) are possible extracted features that could differ between domains (Du et al., 2019).

# Folder structure
- scraper: Notebooks for scraping the following forums:
    - Dark Web Scraper (8chan)
    - Hidden Surface Web Page Scraper (8kun)
    - Surface Web Page Scraper (VGR)

- data: Datasets in csv format and a cleaned parquet for pandas DataFrame.
  - Dark Web Data Set (8chan)
  - Hidden Surface Web Page Data Set (8kun)
  - Surface Web Page Data Set (VGR)

- output: Every analysed forum has:
  - [source]_analysis.parquet: Sentiment Analysis
  - [source]_dictionary: Most common words and ngrams used in the forum, as part of the linguistic Analysis
  - [source]_ldavis_[n]: A visualisation of the topic modelling from the LDA and [n] topics

- utils: Module with auxiliary functions.

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

# Future Work
One popular analysis in the darknet domain is stylometry. As it is more useful in marketplaces rather than forums it was not performed, but it could be an intersting analysis in the future. In marketplaces it is used to track "vendors across marketplaces and in identifying comparable vendors." and to " create a semantic fingerprint which can be used by law enforcement to track or mimic a vendor" (Smith III, 2020). [Maneriker et al. (2021)](https://github.com/pranavmaneriker/sysml) uses a stylometry-based multitask learning approach to this task. 

# Results
All results of the analysis are on the notebook [Text_Analysis.ipynb](https://github.com/octokami/darknet_forum/blob/main/Text_Analysis.ipynb), in their respective areas.

## Implementation
Create the environment with: 

``conda env create -f environment.yml``

``conda activate venv``

## Limitations
The [moderation API from OpenAi](https://platform.openai.com/docs/guides/moderation) was not very effective in this studied case. Two different approaches were tested: post per post analysis and for a whole topic. No content was flagged any of the moderated categories: "hate", "hate/threatening", "self-harm", "sexual", "sexual/minors", "violence", "violence/graphic". Scores were very similarly low across the whole dataset. The documentation of the API explicits that it looks for "hateful, harassing, or violent content that:
- expresses, incites, or promotes hate based on identity
- intends to harass, threaten, or bully an individual
- promotes or glorifies violence or celebrates the suffering or humiliation of others

A hypothesis is that the API only flags things that are extremes in their categories. In special the highest score for hate, albeit barely higher than other samples, was for the post "Remember to keep killing <group of people, redacted>. They are afraid, and they know that they don't have any future.". The example does indeed show hate, but even the second in this category and other categories do not present high scores according to the API.

# References
El Barachi, M., Mathew, S. S., & AlKhatib, M. (2022, July). Combining Named Entity Recognition and Emotion Analysis of Tweets for Early Warning of Violent Actions. In 2022 7th International Conference on Smart and Sustainable Technologies (SpliTech) (pp. 1-6). IEEE.

Evangelatos, P., Iliou, C., Mavropoulos, T., Apostolou, K., Tsikrika, T., Vrochidis, S., & Kompatsiaris, I. (2021, July). Named entity recognition in cyber threat intelligence using transformer-based models. In 2021 IEEE International Conference on Cyber Security and Resilience (CSR) (pp. 348-353). IEEE.

Fu, T., Abbasi, A., & Chen, H. (2010). A focused crawler for Dark Web forums. Journal of the American Society for Information Science and Technology, 61(6), 1213-1231.

Ding, Z., Benjamin, V., Li, W., & Yin, X. (2021, November). Exploring Differences Among Darknet and Surface Internet Hacking Communities. In 2021 IEEE International Conference on Intelligence and Security Informatics (ISI) (pp. 1-3). IEEE.

Du, P. Y., Ebrahimi, M., Zhang, N., Chen, H., Brown, R. A., & Samtani, S. (2019, July). Identifying high-impact opioid products and key sellers in dark net marketplaces: An interpretable text analytics approach. In 2019 IEEE International Conference on Intelligence and Security Informatics (ISI) (pp. 110-115). IEEE.

Maneriker, P., He, Y., & Parthasarathy, S. (2021). SYSML: StYlometry with Structure and Multitask Learning: Implications for Darknet forum migrant analysis. arXiv preprint arXiv:2104.00764.

Nazah, S., Huda, S., Abawajy, J. H., & Hassan, M. M. (2021). An unsupervised model for identifying and characterizing dark web forums. IEEE Access, 9, 112871-112892.

Smith III, J. E., & Hughes, N. E. (2020). Honor Among Thieves: Analyzing Language Features of Darknet Market Vendors. Naval Postgraduate School.
