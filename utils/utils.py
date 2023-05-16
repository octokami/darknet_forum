import random
import time
import openai
import pandas as pd
from tqdm.auto import tqdm  # for notebooks
import gensim
from gensim.models import Phrases
from gensim.models.phrases import Phraser, ENGLISH_CONNECTOR_WORDS

def make_ngrams(corpus_tokenized, n = 4, min_count = 5, threshold = 0.25, scoring=  'npmi'): #'default'
    # higher threshold fewer phrases
    bigram = Phrases(corpus_tokenized, min_count=min_count, threshold=threshold, 
                                   connector_words=ENGLISH_CONNECTOR_WORDS, scoring=scoring) #max_vocab_size 
    bigram_mod = Phraser(bigram)
    if n == 2:
        return bigram, [bigram_mod[doc] for doc in corpus_tokenized]
    
    trigram = Phrases(bigram[corpus_tokenized], threshold=threshold,
                                    connector_words=ENGLISH_CONNECTOR_WORDS, scoring=scoring)
    trigram_mod = Phraser(trigram)
    if n == 3:
        return trigram, [trigram_mod[bigram_mod[doc]] for doc in corpus_tokenized]
    
    quadrigram = Phrases(trigram[bigram[corpus_tokenized]], threshold=threshold,
                                       connector_words=ENGLISH_CONNECTOR_WORDS, scoring=scoring)
    quadrigram_mod = Phraser(quadrigram)
    if n == 4:
        return quadrigram, [quadrigram_mod[trigram_mod[bigram_mod[doc]]] for doc in corpus_tokenized]
    
    else:
        print("Choose n in [2,4]")

def prepare_corpus(corpus_tokenized, keep_n = 10000):
    """
    Input  : Preprocessed documents
    Purpose: Create term dictionary from the corpus and convert list of documents (corpus) into document term matrix
    Output : Term dictionary and Document Term Matrix
    no_below – Keep tokens which are contained in at least no_below documents.
    no_above (float, optional) – Keep tokens which are contained in no more than no_above documents
    (fraction of total corpus size, not an absolute number).
    keep_n (int, optional) – Keep only the first keep_n most frequent tokens.
    """
    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = gensim.corpora.Dictionary(corpus_tokenized)
    
    if keep_n:
        dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=10000)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in corpus_tokenized]

    return dictionary, doc_term_matrix
    
def get_moderation(text, delay = 60):
  """
  """
  try:
    return openai.Moderation.create(input=text, model="text-moderation-latest")["results"][0]
  except:
    time.sleep(delay)
    return openai.Moderation.create(input=text, model="text-moderation-latest")["results"][0]

def add_moderation_to_df(df):
  """
  """
  tqdm.pandas()
  df["moderation"] = df["text"].progress_apply(lambda x: get_moderation(x))

  df["flag"] = df["moderation"].apply(lambda x: x["flagged"]) 
  df["category_scores"] = df["moderation"].apply(lambda x: dict(x["category_scores"])) 
  # Transform the dictionary column into multiple columns
  df[['sexual', 'hate', 'violence', 'self-harm', 'sexual/minors', 'hate/threatening', 'violence/graphic']] = df['category_scores'].apply(lambda x: pd.Series(x))
  df = df.drop(columns="category_scores")
  return df

# define a retry decorator
def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay
        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)
            # Retry on specified errors
            except errors as e:
                # Increment retries
                num_retries += 1
                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())
                # Sleep for the delay
                time.sleep(delay)
            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e
    return wrapper

@retry_with_exponential_backoff
def moderation_with_backoff(**kwargs):
    return openai.Moderation.create(**kwargs)