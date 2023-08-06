#!/usr/bin/env python
from brain_games.cli import (welcome_user, ask_user, get_answer_from_user,
                             compare_answer, congratulate_user, GAME_TRIES)
import random


def is_number_prime(number):
    divider = 2
    while number % divider != 0:
        divider += 1
    return divider == number


def main():
    # welcome user
    username = welcome_user()
    game_lost = False
    for i in range(GAME_TRIES):
        # generate number and answer prime is it
        number = random.randint(0, 100)
        answer = 'yes' if is_number_prime(number) else 'no'

        # ask user is number prime
        ask_user('Answer "yes" if given number is prime.'
                 ' Otherwise answer "no".', number)
        user_answer = get_answer_from_user()

        # compare answer to real one
        if not compare_answer(username, answer, user_answer):
            game_lost = True
            break

    if not game_lost:
        congratulate_user(username)


if __name__ == '__main__':
    main()
