import string
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download("averaged_perceptron_tagger_eng")
nltk.download("stopwords")
nltk.download("wordnet")

class Pipeline():
    def __init__(self, *functions):
        self.factory = functions

    def execute_functions(self, raw: str, output_result=False):
        good = raw
        for function in self.factory:
            good = function(good)
        if output_result:
            print(good)
        return good

def keep_basic_punctuation(tokens):
    white_list = { ".", ",", "'", "?" }
    black_list = set(string.punctuation) - white_list
    return [token for token in tokens if token not in black_list]

def tokenise(text):
    return word_tokenize( " ".join(text.lower().split()))

def pos_tag_speech(tokens):
    return pos_tag(tokens)

def filter_stop_words(tokens):
    stop_words = set(stopwords.words("english"))
    white_list = { "how", "what", "who", "where", "when", "why", "can", "do", "is", "are", "you", "your", "me", "is", "all" }
    return [(token, pos) for token, pos in tokens if token not in stop_words or token in white_list]

def lemmatise_tokens(tokens):
    lemmatiser = WordNetLemmatizer()
    return [lemmatiser.lemmatize(token) for token in tokens]

def lemmatise_pos_tokens(tokens):
    lemmatiser = WordNetLemmatizer()
    # source: https://stackoverflow.com/questions/35870282/nltk-lemmatizer-and-pos-tag
    flatten_pos = lambda t : ("a" if t[0].lower() == "j" else t[0].lower()) if t[0].lower() in ["n", "r", "v"] else "n"
    return [(lemmatiser.lemmatize(token, flatten_pos(pos)), pos) for token, pos in tokens]
