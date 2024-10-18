from lib.lm import lm_init, lm_generate_response
from lib.intent import user_intent
from lib.discoverability import get_random_employee_info
from lib.avatar import dog, cat


# Main conversational loop
lm = lm_init()
while True:
    query = input("USER> ")
    if query.lower() == "exit" or query == ":q":
        print("Goodbye...")
        break

    intent = user_intent(query)
    if intent:
        dog(intent)
        if "get in touch" in intent:
            print(get_random_employee_info())
    else:
        dog(lm_generate_response(lm))
