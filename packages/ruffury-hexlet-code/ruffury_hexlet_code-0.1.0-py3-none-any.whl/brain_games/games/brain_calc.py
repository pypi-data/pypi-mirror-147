#!/usr/bin/env python
from brain_games.cli import (welcome_user, ask_user, get_answer_from_user,
                             compare_answer, congratulate_user, GAME_TRIES)
import random

OPERATORS = ('+', '-', '*')


def get_expression_answer(expression):
    expression_list = expression.split(' ')
    if expression_list[1] == '+':
        return int(expression_list[0]) + int(expression_list[2])
    elif expression_list[1] == '*':
        return int(expression_list[0]) * int(expression_list[2])
    elif expression_list[1] == '-':
        return int(expression_list[0]) - int(expression_list[2])


def main():
    # welcome user
    username = welcome_user()
    game_lost = False
    for i in range(GAME_TRIES):
        # generate expression and calculate answer of it
        expression = f'{str(random.randint(0, 100))} ' \
                     f'{random.choice(OPERATORS)} ' \
                     f'{str(random.randint(0, 100))}'
        expression_answer = str(get_expression_answer(expression))

        # ask user to solve the expression and get answer from him
        ask_user('What is the result of the expression?', expression)
        user_answer = get_answer_from_user()

        # compare answer to real one
        if not compare_answer(username, expression_answer, user_answer):
            game_lost = True
            break

    if not game_lost:
        congratulate_user(username)


if __name__ == '__main__':
    main()
