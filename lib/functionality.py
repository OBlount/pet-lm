# functionality.py
# Contains helper functions to get anything done with the chat-bot

from datetime import datetime

def explicit_confirmation(intent_msg: str) -> bool:
    confirmation = input(intent_msg).lower()
    return (True if confirmation == "yes" else False)

__all__ = [
    "explicit_confirmation",
    "set_username",
    "update_username",
    "set_pet_name",
    "set_favourite_pet",
    "initiate_booking",
    "show_bookings",
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

def initiate_booking(dbm, user_id):
    pet_name = dbm.get_pet_name(user_id)
    pet_type = dbm.get_favourite_animal(user_id) if dbm.get_favourite_animal(user_id) else "pet"

    print(f"Sure, let's book an appointment for your {pet_type} named {pet_name}.")
    confirmation = explicit_confirmation("Is this correct? (yes/no): ")

    if not confirmation:
        print("Booking process canceled. Please let me know if you'd like to try again.")
        return

    while True:
        date = input(f"What date would you like to book your appointment with {pet_name}? (dd/mm/yyyy): ")
        if date == "quit":
            break

        # Validate date format
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format. Please enter the date in the format dd/mm/yyyy.")
            continue

        # Retrieve available slots for the chosen date
        print(f"You have chosen the date: {date}")
        slots = dbm.get_booking_slots(date)
        if not slots:
            print(f"Sorry, no slots are available for {date}. Please choose another date. Or quit by typing 'quit'")
            continue

        print(f"Available slots for {date}:")
        for i, slot in enumerate(slots, 1):
            print(f"\t{i} \tTime: {slot[1]}, Specialist: {slot[2]}, For: {slot[3]}")

        # Let the user select a slot
        try:
            slot_choice = int(input("Choose an option using: (1 or 2 or 3) "))
            if 1 <= slot_choice <= len(slots):
                chosen_slot = slots[slot_choice-1]
            else:
                print("Invalid choice. Try again")
                continue
        except ValueError:
            print("Invalid input. Try again")
            continue

        print(f"You have chosen {chosen_slot[1]} on {date} with {chosen_slot[2]}.")
        final_confirmation = explicit_confirmation("Would you like to confirm this booking? (yes/no): ")

        if final_confirmation:
            dbm.insert_booking(user_id, chosen_slot[0])
            print("Your appointment has been booked successfully!")
            print("Would you like to anything else?")
            break
        else:
            print("Booking process canceled. Please let me know if you'd like to try again.")
            break

def show_bookings(dbm, user_id):
    bookings = dbm.get_user_bookings(user_id)
    if bookings:
        print(f"You have the following bookings:")
        for booking in bookings:
            print(f"\tDate: {booking['appointment_date']}, Time: {booking['appointment_time']}, with specialist: {booking['specialist_name']}")
    else:
        print(f"You have no bookings.")
