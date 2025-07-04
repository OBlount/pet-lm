import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Compute user query intent using tf-idf and cosine similarity
def user_intent(user_input):
    if not user_input:
        return None

    df = pd.read_csv("data/intentMap.csv", sep='|')

    intents = df["Intent"].astype(str).tolist()
    responses = df["Response"].astype(str).tolist()

    vectoriser = TfidfVectorizer()
    tfidf_matrix = vectoriser.fit_transform(intents)
    user_tfidf = vectoriser.transform([" ".join([token for token, tag in user_input])])

    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    intent_index = cosine_similarities.argmax()
    similarity_score = cosine_similarities[intent_index]

    if similarity_score > 0.4:
        return responses[intent_index]
    else:
        return None
