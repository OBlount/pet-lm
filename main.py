from lib.db import DBManager
from lib.pipeline import Pipeline, tokenise, keep_basic_punctuation, pos_tag_speech, filter_stop_words, lemmatise_pos_tokens
from lib.intent import user_intent
from lib.discoverability import get_random_employee_info, get_help_menu
from lib.sentiment import SentimentAnalyser
from lib.avatar import default_avatar, dog, cat


dbm = DBManager()

avatar_print = default_avatar
avatar_print("Hi, I can help you with booking an appointment with us. Let's start with your name?")
user_id = None
while True:
    username = input("What is your name: ")
    confirm = input(f"Your name is {username}. Is this correct? (yes/no): ").lower()
    if confirm == "yes":
        user_id = dbm.insert_username(username)
        favourite_animal = input("What is your pet? (dog, cat..): ")
        dbm.update_favourite_animal(favourite_animal, user_id)
        if favourite_animal.lower() == "dog":
            avatar_print = dog
        elif favourite_animal.lower() == "cat":
            avatar_print = cat
        else:
            avatar_print = default_avatar
        break

# Create custom NLP pipeline
pipeline = Pipeline(
        tokenise,
        keep_basic_punctuation,
        pos_tag_speech,
#       filter_stop_words,
        lemmatise_pos_tokens,
)

sentimentAnalyser = SentimentAnalyser()

# Main conversational loop
while True:
    query = input(f"{dbm.get_username(user_id)}> ")
    if query.lower() == "exit" or query == ":q":
        avatar_print(f"Goodbye {dbm.get_username(user_id)}...")
        break

    query = pipeline.execute_functions(query)
    sentimentAnalyser.process_user_query(sentimentAnalyser.load_sentiment_model(), query)
    chatbot_response = user_intent(query)

    if chatbot_response:
        if "your name" in chatbot_response:
            avatar_print(chatbot_response + f" Your name is {dbm.get_username(user_id)}.")
        elif "help menu" in chatbot_response:
            avatar_print(chatbot_response)
            print(get_help_menu())
        elif "meet our team" in chatbot_response:
            avatar_print(chatbot_response)
            print(get_random_employee_info())
        else:
            avatar_print(chatbot_response)
    else:
        avatar_print("Sorry, I don't quite know how to answer that")

    # Append a message onto the response to help the user having trouble
    if sentimentAnalyser.get_sentiment() == -3:
        print("\nI've noticed that you might not be enjoying your booking experience. If you need any assistance then ask anytime for help")
        print("\nOr get in contact with our customer support online. Thank-you for being patient with us.")

# Clean
del dbm
