from lib.lm import lm_init, lm_generate_response
from lib.avatar import dog, cat


# Main conversational loop
lm = lm_init()
while True:
    query = input("USER> ")
    if query.lower() == "exit" or query == ":q":
        print("Goodbye...")
        break

    dog(lm_generate_response(lm))
