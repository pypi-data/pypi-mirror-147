#!/usr/bin/env python
from brain_games.cli import (welcome_user, ask_user, get_answer_from_user,
                             compare_answer, congratulate_user, GAME_TRIES)
import random


def generate_progression():
    progression_len = random.randint(5, 10)
    first_element = random.randint(0, 100)
    step = random.randint(1, 10)
    last_element = first_element + (step * progression_len)
    return list(range(first_element, last_element, step))


def hide_element_in_progression(progression, answer):
    progression_str = [str(i) for i in progression]
    answer_index = progression_str.index(answer)

    return ' '.join([*progression_str[:answer_index],
                     *['..'],
                     *progression_str[answer_index + 1:]])


def main():
    # welcome user
    username = welcome_user()
    game_lost = False
    for i in range(GAME_TRIES):
        # generate progression and choose one hidden number
        progression = generate_progression()
        answer = str(random.choice(progression))
        user_progression = hide_element_in_progression(progression, answer)

        # ask user to find the hidden number
        ask_user('What number is missing in the progression?', user_progression)
        user_answer = get_answer_from_user()

        # compare answer to real one
        if not compare_answer(username, answer, user_answer):
            game_lost = True
            break

    if not game_lost:
        congratulate_user(username)


if __name__ == '__main__':
    main()
