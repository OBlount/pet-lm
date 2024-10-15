import csv
import nltk

from nltk import word_tokenize, sent_tokenize
from nltk.util import pad_sequence
from nltk.lm import MLE, Laplace
from collections import Counter
from nltk.lm.preprocessing import pad_both_ends, padded_everygram_pipeline

# Download nltk resources
nltk.download("punkt_tab")

document = ""
with open("dataset.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        document += row[1] + ' '

n_param = 4
tokenized = [word_tokenize(sent) for sent in sent_tokenize(document)]
corpus, vocab = padded_everygram_pipeline(n_param, tokenized)
lm = Laplace(n_param)
lm.fit(corpus, vocab)

print ("Size of vocabulary: ", str(len(lm.vocab)))

gen = lm.generate(50)
print(" ".join(gen). replace("<s>", "").replace("</s>", ""))
