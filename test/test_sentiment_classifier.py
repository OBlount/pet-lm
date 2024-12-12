import pandas as pd
import pickle

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def load_sentiment_model():
    model = None
    with open("../data/sentiment_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# Load the dataset
data = pd.read_csv("../data/training.1600000.processed.noemoticon.csv", encoding="latin1", header=None)
data.columns = ["target", "ids", "date", "flag", "user", "text"]
label_mapping = {0: "negative", 2: "neutral", 4: "positive"}
data["target"] = data["target"].map(label_mapping)
x = data["text"]
y = data["target"]

# Load model
classifier = load_sentiment_model()
predictions = classifier.predict(x)

# Evaluate performance
print("Confusion Matrix:")
print(confusion_matrix(y, predictions))
print("\nClassification Report:")
print(classification_report(y, predictions))
print("\nAccuracy:")
print(f"{accuracy_score(y, predictions) * 100:.2f}%")
