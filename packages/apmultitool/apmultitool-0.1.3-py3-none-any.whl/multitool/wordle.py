#! /usr/bin/python3
import json
import shutil


def filter_word(word, hints, pos, wrong, correct):
    for char in wrong:
        if char in word:
            return False
    for i in range(len(word)):
        if word[i] in pos[i]:
            return False
    for char in hints:
        if char not in word:
            return False
    for j in range(len(correct)):
        if correct[j] != "":
            if word[j] != correct[j]:
                return False
    return True


def interpret_results(hints, wrong, correct, pos, l, guess):
    result = input(guess + "- Results?(W/C/H) \n")
    if len(result) != l:
        return interpret_results(hints, wrong, correct, pos, l, guess)
    decypher_input(hints, wrong, correct, pos, guess, result)


def decypher_input(hints, wrong, correct, pos, guess, result):
    for i, char in enumerate(result):
        if char in "wW":
            if guess[i] in correct:
                pos[i] += guess[i]
            else:
                wrong.add(guess[i])
        elif char in "cC":
            hints.add(guess[i])
            correct[i] = guess[i]
        elif char in "hH":
            pos[i] += guess[i]
            hints.add(guess[i])


def get_frequencies(words):
    f = {}
    for word in words:
        for char in word:
            if char not in f:
                f[char] = 1
            else:
                f[char] += 1
    return [i for i, _ in sorted(list(f.items()), key=lambda x: x[1], reverse=True)]


def filter_ideal(words):
    picked = []
    freq = get_frequencies(words)
    for word in words:
        ranks = [freq.index(i) for i in word]
        counts = [word.count(i) for i in word]
        if sum(counts) == len(word) and sum(ranks) < (0.75 * len(ranks)) * len(ranks):
            picked.append(word)
    return picked


def get_choice(choices):
    cols = shutil.get_terminal_size().columns
    output, leng = "", 0
    for i, choice in enumerate(choices):
        text = f"{i}: {choice},   "
        if len(text) + leng < cols:
            output += text
            leng += len(text)
        else:
            output += "\n" + text
            leng = len(text)
    print(output)
    choice = input("Choose or enter a word.\n")
    if choice.isdigit():
        return choices[int(choice)]
    return choice


def get_words(l):
    return [i for i in json.load(open("assets/Words_Length.json")) if len(i) == l]


def filter_words(words=None, l=5):
    if not words:
        words = get_words(l)
    starters = filter_ideal(words)
    return starters


def solve(l=5):
    hints = set()
    wrong = set()
    correct = ["" for i in range(l)]
    pos = {i: "" for i in range(l)}
    words = get_words(l)
    starters = filter_words(words)
    guess = get_choice(starters)
    count = 1
    while True:
        interpret_results(hints, wrong, correct, pos, l, guess)
        for word in words[::-1]:
            if not filter_word(word, hints, pos, wrong, correct):
                words.remove(word)
        if count > 2 or len(words) < 50:
            guess = get_choice(words)
        else:
            guess = get_choice(filter_ideal(words))
        count += 1
