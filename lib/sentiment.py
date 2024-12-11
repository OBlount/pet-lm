import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

class SentimentAnalyser():
    def __init__(self):
        self.emotional_metric = 0

    def load_sentiment_model(self):
        model = None
        with open("data/sentiment_model.pkl", "rb") as file:
            model = pickle.load(file)
        return model

    def process_user_query(self, model, user_input):
        prediction = model.predict([" ".join([token for token, tag in user_input])])[0]
        self.adjust_emotion(prediction)

    def adjust_emotion(self, sentiment):
        if sentiment == "positive":
            self.emotional_metric = min(self.emotional_metric+1, 6)
        elif sentiment == "negative":
            self.emotional_metric = max(self.emotional_metric-2, -3)
        else:
            pass

    def get_sentiment(self):
        return self.emotional_metric

def train_and_save():
    # https://www.kaggle.com/datasets/kazanova/sentiment140?resource=download
    data = pd.read_csv("../data/training.1600000.processed.noemoticon.csv", encoding="latin1", header=None)
    data.columns = ["target", "ids", "date", "flag", "user", "text"]
    label_mapping = { 0: "negative", 2: "neutral", 4: "positive" }
    data["target"] = data["target"].map(label_mapping)
    x = data["text"]
    y = data["target"]
    x_subset, _, y_subset, _ = train_test_split(x, y, test_size=0.99, random_state=42)
    pipeline = make_pipeline(TfidfVectorizer(stop_words="english", max_features=10000), MultinomialNB())
    pipeline.fit(x_subset, y_subset)
    print("Saving model...")
    with open("../data/sentiment_model.pkl", "wb") as file:
        pickle.dump(pipeline, file)
    print("Model saved")

if __name__ == "__main__":
    train_and_save_model()
