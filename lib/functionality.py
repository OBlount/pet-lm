# functionality.py
# Contains helper functions to get anything done with the chat-bot

__all__ = [
    "set_username",
    "update_username",
    "set_pet_name",
    "set_favourite_pet",
        ]

from lib.avatar import default_avatar, dog, cat

def set_username(dbm):
    while True:
        username = input("What is your name: ")
        confirm = input(f"Your name is {username}. Is this correct? (yes/no): ").lower()
        if confirm == "yes":
            user_id = dbm.insert_username(username)
            return user_id

def update_username(dbm, user_id):
    while True:
        username = input("What is your name: ")
        confirm = input(f"Your name is {username}. Is this correct? (yes/no): ").lower()
        if confirm == "yes":
            dbm.update_username(username, user_id)
            break

def set_pet_name(dbm, user_id):
    while True:
        pet_name = input("What is your pet name: ")
        confirm = input(f"Your pet's name is {pet_name}. Is this correct? (yes/no): ").lower()
        if confirm == "yes":
            dbm.update_pet_name(pet_name, user_id)
            break

def set_favourite_pet(dbm, user_id):
    favourite_animal = input("What is your pet? (dog, cat..): ")
    dbm.update_favourite_animal(favourite_animal, user_id)
    if favourite_animal.lower() == "dog":
        return dog
    elif favourite_animal.lower() == "cat":
        return cat
    else:
        return default_avatar
