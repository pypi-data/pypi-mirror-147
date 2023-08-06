#!/usr/bin/env python
from brain_games.cli import (welcome_user, ask_user, get_answer_from_user,
                             compare_answer, congratulate_user, GAME_TRIES)
import random


def gcd(a, b):
    if a == 0 or b == 0:
        return max(a, b)
    else:
        if a > b:
            return gcd(a % b, b)
        else:
            return gcd(a, b % a)


def get_expression_answer(expression):
    expression_list = expression.split(' ')
    a, b = int(expression_list[0]), int(expression_list[1])
    return gcd(a, b)


def main():
    # welcome user
    username = welcome_user()
    game_lost = False
    for i in range(GAME_TRIES):
        # generate two numbers and find gcd of it
        expression = f'{str(random.randint(0, 100))} ' \
                     f'{str(random.randint(0, 100))}'
        expression_answer = str(get_expression_answer(expression))

        # ask user to find gcd of two numbers
        ask_user('Find the greatest common '
                 'divisor of given numbers.', expression)
        user_answer = get_answer_from_user()

        # compare answer to real one
        if not compare_answer(username, expression_answer, user_answer):
            game_lost = True
            break

    if not game_lost:
        congratulate_user(username)


if __name__ == '__main__':
    main()
