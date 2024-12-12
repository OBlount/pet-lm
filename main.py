import random

from lib.db import DBManager
from lib.pipeline import Pipeline, tokenise, keep_basic_punctuation, pos_tag_speech, filter_stop_words, lemmatise_pos_tokens
from lib.functionality import *
from lib.intent import user_intent
from lib.discoverability import get_random_employee_info, get_help_menu
from lib.sentiment import SentimentAnalyser
from lib.markers import conversational_markers
from lib.avatar import default_avatar


dbm = DBManager()

avatar_print = default_avatar
avatar_print("Hi, I can help you with booking an appointment with us. Let's start with your name?")
user_id = None

# First, get user information
user_id = set_username(dbm)
set_pet_name(dbm, user_id)
avatar_print = set_favourite_pet(dbm, user_id)

# Create custom NLP pipeline
pipeline = Pipeline(
        tokenise,
#        keep_basic_punctuation,
        pos_tag_speech,
#       filter_stop_words,
#        lemmatise_pos_tokens,
)

sentimentAnalyser = SentimentAnalyser()

# Main conversational loop
while True:
    query = input(f"{dbm.get_username(user_id)}> ")

    query = pipeline.execute_functions(query)
    sentimentAnalyser.process_user_query(sentimentAnalyser.load_sentiment_model(), query)
    chatbot_response = user_intent(query)

    # Intents/Functions
    if chatbot_response:
        if "Goodbye" in chatbot_response:
            avatar_print(f"{random.choice(conversational_markers['goodbyes'])} {dbm.get_username(user_id)}...")
            quit()
        elif "Hello!" in chatbot_response:
            avatar_print(f"{random.choice(conversational_markers['greetings'])}, {dbm.get_username(user_id)}...")
        elif "your name" in chatbot_response:
            avatar_print(chatbot_response + f" Your name is {dbm.get_username(user_id)}.")
        elif "help menu" in chatbot_response:
            avatar_print(chatbot_response)
            print(get_help_menu())
        elif "meet our team" in chatbot_response:
            avatar_print(chatbot_response)
            print(get_random_employee_info())
        elif "change my name" in chatbot_response:
            if explicit_confirmation(f"You have chosen to change your username, {random.choice(conversational_markers['confirmation_follow_up'])}? (yes/no): "):
                update_username(dbm, user_id)
        elif "change my pet's name" in chatbot_response:
            if explicit_confirmation(f"You have chosen to change your pet's name, {random.choice(conversational_markers['confirmation_follow_up'])}? (yes/no):"):
                set_pet_name(dbm, user_id)
        elif "change my favourite pet preference" in chatbot_response:
            if explicit_confirmation(f"You have chosen to change your avatar, {random.choice(conversational_markers['confirmation_follow_up'])}? (yes/no): "):
                avatar_print = set_favourite_pet(dbm, user_id)
        elif "book an appointment" in chatbot_response:
            if explicit_confirmation(f"You have chosen to book an appointment, {random.choice(conversational_markers['confirmation_follow_up'])}? (yes/no): "):
                initiate_booking(dbm, user_id)
        elif "get your bookings" in chatbot_response:
            if explicit_confirmation(f"You have chosen to look at bookings, {random.choice(conversational_markers['confirmation_follow_up'])}? (yes/no): "):
                show_bookings(dbm, user_id)
        else:
            avatar_print(chatbot_response)
    else:
        avatar_print(f"Sorry, I don't quite know how to answer that, {random.choice(conversational_markers['clarifications_questions'])}?")

    # Append a message onto the response to help the user having trouble
    if sentimentAnalyser.get_sentiment() == -8:
        print("\nI've noticed that you might not be enjoying your booking experience. If you need any assistance then ask anytime for help")
        print("\nOr get in contact with our customer support online. Thank-you for being patient with us.")

# Clean
del dbm
