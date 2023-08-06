import prompt

GAME_TRIES = 3


def welcome_user():
    print('Welcome to the Brain Games!')
    name = prompt.string('May I have your name? ')
    print(f'Hello, {name}!')
    return name


def ask_user(question_text, question_task):
    print(question_text)
    print(f'Question: {question_task}')


def get_answer_from_user():
    answer = prompt.string('Your answer: ')
    return answer


def compare_answer(username, real_answer, user_answer):
    if real_answer == user_answer:
        print('Correct')
        return True
    else:
        print(f"'{user_answer}' is wrong answer ;(. "
              f"Correct answer was '{real_answer}'.")
        print(f"Let's try again, {username}!")
        return False


def congratulate_user(name):
    print(f'Congratulations, {name}!')
