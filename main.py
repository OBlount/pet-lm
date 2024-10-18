from lib.db import DBManager
from lib.lm import lm_init, lm_generate_response
from lib.intent import user_intent
from lib.discoverability import get_random_employee_info
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

# Main conversational loop
lm = lm_init()
while True:
    query = input(f"{dbm.get_username(user_id)}> ")
    if query.lower() == "exit" or query == ":q":
        avatar_print(f"Goodbye {dbm.get_username(user_id)}...")
        break

    intent = user_intent(query)
    if intent:
        avatar_print(intent)
        if "get in touch" in intent:
            print(get_random_employee_info())
    else:
        avatar_print(lm_generate_response(lm))

# Clean
del dbm
