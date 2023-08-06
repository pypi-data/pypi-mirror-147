#!/usr/bin/env python
from brain_games.cli import (welcome_user, ask_user, get_answer_from_user,
                             compare_answer, congratulate_user, GAME_TRIES)
import random


def main():
    # Welcome gamer
    username = welcome_user()
    game_lost = False
    for i in range(GAME_TRIES):
        # generate number
        number = random.randint(0, 100)
        answer = 'yes' if number % 2 == 0 else 'no'

        # ask user to get answer from him
        ask_user('Answer "yes" if the number is even, '
                 'otherwise answer "no".', number)
        user_answer = get_answer_from_user()

        # compare answer to real one
        if not compare_answer(username, answer, user_answer):
            game_lost = True
            break

    if not game_lost:
        congratulate_user(username)


if __name__ == '__main__':
    main()
