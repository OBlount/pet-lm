import os
import csv
import nltk

from nltk import word_tokenize, sent_tokenize
from nltk.util import pad_sequence
from nltk.lm import MLE, Laplace
from collections import Counter
from nltk.lm.preprocessing import pad_both_ends, padded_everygram_pipeline
from joblib import dump, load


# Download nltk resources
nltk.download("punkt_tab")
csv.field_size_limit(10*1024*1024)

# Load up a pre-existing lm or produce one using the data/dataset.csv
def lm_init():
    if os.path.isfile("data/lm.joblib"):
        return lm_load()

    document = ""
    n_param = 2
    try:
        with open("data/dataset.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="|")
            next(reader)
            for row in reader:
                document += row[1] + ' '
    except Exception as e:
        print(f"Error with the dataset: {e}")
        quit(1)
    tokenized = [word_tokenize(sent) for sent in sent_tokenize(document)]
    corpus, vocab = padded_everygram_pipeline(n_param, tokenized)
    lm = Laplace(n_param)
    lm.fit(corpus, vocab)

    lm_save(lm)
    return lm

# Dump lm to disk
def lm_save(lm):
    dump(lm, "data/lm.joblib")

# Load lm from disk
def lm_load():
    return load("data/lm.joblib")

# Generate and format natural language
def lm_generate_response(lm):
    gen = lm.generate(50)
    return (" ".join(gen). replace("<s>", "").replace("</s>", "").strip())
