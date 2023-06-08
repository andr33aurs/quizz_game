import json
import os
import random
import time

import caesar
import datetime

MENU = """
Hello admin! What would you like to do?
\t\t1. Add question
\t\t2. Remove question
\t\t3. Edit question
\t\t4. Add player
\t\t5. Exit
\t\t6. Remove player
"""
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAILRED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'


def check_userpass(users: dict, username: str, password: str) -> bool:
    if username == 'admin':
        admin_pass = os.environ['admin_quiz'].split("~")[1]
        if password == admin_pass:
            return True

    if username in users.keys():
        if decrypt_password(password, users[username]):
            return True
        else:
            print("Parola este gresita")
            return False

    else:
        print("Username ul nu se afla in baza de date")
        return False

# OPTION 3 edit question
def edit_question(questions):
    questions_list = questions['questions']
    for index, question in enumerate(questions_list):
        print(f"{str(index)}. {question['question']}")
    question_id = input("Please choose which question would you like to remove: ")

    questions_list[int(question_id)] = {'question': input("Citeste o noua intrebare:\n"),
                                        'answers': input("Citeste lista de raspunsuri separate prin ~: \n").split("~"),
                                        "correctIndex": int(input("Citeste index raspusului corect:\n"))}
    print()
    with open("questions.json", "w") as file:
        new_json_string = json.dumps(questions, indent=4)
        file.write(new_json_string)


#OPTION 2 remove questions in the quiz
def remove_question(questions):
    questions_list = questions['questions']
    for index, question in enumerate(questions_list):
        print(f"{str(index)}. {question['question']}")
    question_id = input("Please choose which question would you like to remove: ")

    del questions_list[int(question_id)]
    print()
    with open("questions.json", "w") as file:
        new_json_string = json.dumps(questions, indent=4)
        file.write(new_json_string)





    # questions = {"questions": questions}



# OPTION 4 add player
def add_player(users):

    username = input("Adauga noul jucator: ")
    while username in users.keys():
        username = input("Jucatorul deja exista,"
                         " adauga alt jucator sau exit pentru revenire la meniu: ")
        if username == "exit":
            break

    if username == "exit":
        print("Admin ul a renuntat sa adauge un jucator nou.")
        return

    password = input("Adauga parola lui: ")
    # username = "vlad"
    # password = "abc"
    now = datetime.datetime.now()
    key = now.second % 10
    while key == 0:
        time.sleep(random.randint(1, 5))
        now = datetime.datetime.now()
        key = now.second % 10

    password = caesar.encrypt(password, key)
    users[username] = {"password": password, "high_score": 0, "date": str(now)}

    with open("users.json", "w") as file:
        new_json_string = json.dumps(users, indent=4)
        file.write(new_json_string)



def read_file(path):
    with open(path, "r") as f:
        try:
            config_dict = f.read()
            config_dict = json.loads(config_dict)
        except Exception as e:
            print(f"Aceasta e o exceptie la transformarea in dictionar {e}")
    return config_dict


def read_config(*paths):
    my_list = []
    for index, path in enumerate(paths):
        with open(path, "r") as f:
            try:
                config_dict = f.read()
                config_dict = json.loads(config_dict)
            except Exception as e:
                print(f"Aceasta e o exceptie la transformarea in dictionar {e}")
        my_list.append(config_dict)

    return my_list[0], my_list[1]


def add_question(questions):
    new_question = input("Introduceti noua intrebare: ")
    answers = input("Variante de raspunse separate prin ~: ")
    answers = answers.split("~")
    for index, answer in enumerate(answers):
        print(f"{str(index)}.{answer}")
    correct_index = int(input("Index ul pentru raspunsul corect este: "))

    questions['questions'].append({"question": new_question, "answers": answers,
                                   "correctIndex": correct_index})

    with open("questions.json", "w") as file:
        new_json_string = json.dumps(questions, indent=4)
        file.write(new_json_string)


def run_game(questions, users, player):
    score = 0
    print(f"Hello {player}. Welcome to the game!!!")
    questions = questions['questions']
    for question in questions:
        print(question['question'])
        possible_answers_string = ''
        for index, answer in enumerate(question['answers']):
            possible_answers_string += f"{str(index+1)}. {answer}\n"
        print(f"Possible answers are: \n{possible_answers_string}")
        user_response = input("Introdu cifra cu raspunsul corect ")
        if int(user_response) - 1 == question['correctIndex']:
            print(OKGREEN + "Congrats that's the correct answer\n\n" + ENDC)
            time.sleep(2)
            score += 1
        else:
            correct_index = question['correctIndex']
            correct_response = question['answers'][correct_index]
            print(FAILRED + f"Wrong. The correct answer was {correct_response}\n\n" + ENDC)
            time.sleep(2)
    if users[player]['high_score'] < score:
        print(OKBLUE + f"Congrats {player}!!! Your new high score is {score}" + ENDC)
        users[player]['high_score'] = score
        with open("users.json", "w") as file:
            new_json_string = json.dumps(users, indent=4)
            file.write(new_json_string)


def decrypt_password(password_read_by_user, user):
    key = user['date'].split(".")[0][-1]
    decrypted_password = caesar.decrypt(user['password'], int(key))
    if password_read_by_user == decrypted_password:
        return True
    else:
        return False


if __name__ == "__main__":
    # users = read_file("users.json")
    # questions = read_file("questions.json")
    users, questions = read_config("users.json", "questions.json")
    user = input("Va rog sa introduceti username ul: ")
    passwd = input("Va rog introduceti parola: ")

    if check_userpass(users, username=user, password=passwd):
        if user == 'admin':
            while True:
                print(MENU)
                command = input()
                match command:
                    case "1":
                        print("Add question")
                        add_question(questions)

                    case "2":
                        print("Remove question")
                        remove_question(questions)
                    case "3":
                        print("Edit question")
                        edit_question(questions)
                    case "4":
                        print("Add player")
                        add_player(users)
                    case "5":
                        print("Adminul a ales sa paraseasca programul.")
                        break
                print("\n\n\n\n")
        else:
            run_game(questions, users, user)



    else:
        print("Autentificare esuata")




