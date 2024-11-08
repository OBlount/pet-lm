import random

# Document an employee
def groomer_document_structuring(groomer):
    return {
            "introduction": [groomer["name"], groomer["role "], groomer["experience "]],
            "specialisations": [groomer["specialisations"], groomer["favorite_breeds"]],
            "services": groomer["pet_types"],
            "personal_info": [groomer["hobbies"]],
    }

# Aggregate all the info we need for an employee biography
def groomer_aggregation(structured_groomer):
    aggregation = {}

    aggregation["introduction"] = f"{structured_groomer['introduction'][0]}, a {structured_groomer['introduction'][1]} with {structured_groomer['introduction'][2]} years of experience, specialises in {structured_groomer['specialisations'][0]}."

    pet_types = " and ".join(structured_groomer["services"])
    aggregation["skills"] = f"they are skilled at grooming {pet_types}."

    hobbies = ", ".join(structured_groomer["personal_info"][0][:-1]) + " and " + structured_groomer["personal_info"][0][-1]
    aggregation["personal"] = f"they enjoy {hobbies}."

    favourite_breeds = " and ".join(structured_groomer["specialisations"][1])
    aggregation["breeds"] = f"{structured_groomer['introduction'][0]}'s favourite breeds are {favourite_breeds}."

    return aggregation

# Seemless connection between aggregated sentences
def groomer_realisation(groomer):
    intro = groomer["introduction"]
    skills = "Note that " + groomer["skills"]
    personal = "When away from grooming, " + groomer["personal"]
    breeds = "Do you have a favourite breed? " + groomer["breeds"]
    return f"{intro} {skills} {personal} {breeds}"

# Print the entire employee list
def get_random_employee_info():
    employee = employees[random.randrange(len(employees))]
    structured = groomer_document_structuring(employee)
    aggregated = groomer_aggregation (structured)
    final_output = groomer_realisation(aggregated)
    return final_output

# Document the help instructions
def help_document_structuring(help_command):
    return {
            "lead": [help_command["lead"]],
            "briefing": [help_command["command"], help_command["description"]],
    }

# Aggregate all the info we need for the help menu
def help_aggregation(structured_help):
    aggregation = {}
    aggregation["lead"] = f"{structured_help['lead'][0]}! "
    aggregation["briefing"] = f"{structured_help['briefing'][0]} \n\t - {structured_help['briefing'][1]}"
    return aggregation

# Seemless connection between aggregated sentences
def help_realisation(help_menu):
    lead = help_menu["lead"]
    briefing = "The command to do this is: " + help_menu["briefing"] + "\n\n"
    return f"{lead} {briefing}"

# Print the entire employee list
def get_help_menu():
    final_output = ""
    for cmd in help_menu:
        structured = help_document_structuring(cmd)
        aggregated = help_aggregation(structured)
        final_output = final_output + help_realisation(aggregated)
    end = "Please take note of what I can do for you. If you are in any doubt, please type 'help' to get these tips up again."
    return final_output + end

# Employees that the user can get to know more of
employees = [
        {
            "name": "Aisha",
            "role ": "Pet Groomer",
            "experience ": "5 years",
            "expertise ": "dog grooming",
            "hobbies": ["painting", "hiking"],
            "specialisations": "poodle cuts",
            "favorite_breeds": ["poodle", "golden retriever"],
            "pet_types": ["dogs", "cats"]
        },
        {
            "name": "Lila",
            "role ": "Pet Groomer",
            "experience ": "3 years",
            "expertise ": "cat grooming",
            "hobbies": ["reading", "cooking"],
            "specialisations": "persian grooming",
            "favorite_breeds": ["persian", "sphynx"],
            "pet_types": ["cats", "rabbits"]
        },
        {
            "name": "Mei-Ling",
            "role ": "Pet Groomer",
            "experience ": "7 years",
            "expertise ": "all breeds grooming",
            "hobbies": ["yoga", "traveling"],
            "specialisations": "exotic breeds",
            "favorite_breeds": ["bulldog", "beagle"],
            "pet_types": ["dogs", "ferrets"]
        },
        {
            "name": "Carlos",
            "role ": "Pet Groomer",
            "experience ": "4 years",
            "expertise ": "senior pet grooming",
            "hobbies": ["photography", "cycling"],
            "specialisations": "senior dog grooming",
            "favorite_breeds": ["chihuahua", "dachshund"],
            "pet_types": ["dogs", "cats", "hamsters"]
        }
]

# Help hints and chatbot function discoverability
help_menu = [
        {
            "command": "hello",
            "description": "Say hello to the bot.",
            "lead": "I can greet"
        },
        {
            "command": "help",
            "description": "Learn more about the company and chatbot features",
            "lead": "I can provide info"
        },
        {
            "command": "pet care",
            "description": "Get tips on how to take care of your pet.",
            "lead": "I can assist in pet health and care"
        },
        {
            "command": "grooming services",
            "description": "Find out about the grooming services offered.",
            "lead": "I can inform you about our pet grooming services"
        },
        {
            "command": "book appointment",
            "description": "Schedule an appointment for grooming.",
            "lead": "I can book and appointment"
        },
        {
            "command": "contact",
            "description": "Get contact information for support.",
            "lead": "I can connect you with our amazing staff"
        }
]
