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

def lm_init():
    if os.path.isfile("lm.joblist"):
        return lm_load("lm.joblist")

    document = ""
    n_param = 4
    try:
        with open("data/dataset.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                document += row[1] + ' '
    except:
        print("Error with the dataset")
        quit(1)
    tokenized = [word_tokenize(sent) for sent in sent_tokenize(document)]
    corpus, vocab = padded_everygram_pipeline(n_param, tokenized)
    lm = Laplace(n_param)
    lm.fit(corpus, vocab)

    lm_save(lm)
    return lm

def lm_save(lm):
    dump(lm, "data/lm.joblib")

def lm_load():
    return load("data/lm.joblib")

def lm_generate_response(lm):
    gen = lm.generate(50)
    return (" ".join(gen). replace("<s>", "").replace("</s>", "").strip())
