import pandas as pd
import numpy as np

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

seed = 123

classifiers = {
    "Multinomial Naive Bayes": MultinomialNB(),
    "Support Vector Machine": SVC(),
    "Random Forest": RandomForestClassifier()
}

# Load the dataset
data = pd.read_csv("../data/training.1600000.processed.noemoticon.csv", encoding="latin1", header=None)
data.columns = ["target", "ids", "date", "flag", "user", "text"]
label_mapping = {0: "negative", 2: "neutral", 4: "positive"}
data["target"] = data["target"].map(label_mapping)
x = data["text"]
y = data["target"]

x_subset, _, y_subset, _ = train_test_split(x, y, test_size=0.99, random_state=seed)

kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)

print("Comparing classifiers")
results = {}
for name, classifier in classifiers.items():
    pipeline = make_pipeline(TfidfVectorizer(stop_words="english", max_features=10000), classifier)
    scores = cross_val_score(pipeline, x_subset, y_subset, cv=kfold, scoring="accuracy")
    results[name] = scores
    print(f"{name}:")
    print("Cross-validation scores:", scores)
    print("Average accuracy:", np.mean(scores), '\n')

print("Summary of classifier performance:")
for name, scores in results.items():
    print(f"{name}: Average Accuracy = {np.mean(scores):.4f}")

