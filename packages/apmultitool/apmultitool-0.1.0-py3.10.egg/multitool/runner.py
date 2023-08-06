import json
import os
import sys

from multitool.win import start_gui
from multitool.wordle import solve


class Words:
    """
    Namespace containing reference documents for gathering data.
    """

    all_words = json.load(open("assets/Words_Length.json"))
    word_frequencies = json.load(open("assets/Words_Frequency.json"))
    synonyms = json.load(open("assets/Synonyms.json"))


def sanatize(input):
    """
    Convert input command line arguments into format contained by documents.
    """
    return input.upper()


def show(output):
    """
    Format the output to show user on console screen.
    """
    sys.stdout.write("Results: ")
    space = max([len(i) for i in output])
    try:
        size = os.get_terminal_size().columns
    except:
        size = 80
    space = space + 1 + len(str(len(output))) + 2
    cols, counter = size // space, 0
    while counter < len(output):
        line = ""
        if len(output) - counter < cols:
            cols = len(output) - counter
        for i in range(cols):
            word = output[counter].ljust(space, " ")
            phrase = f"{str(i).rjust(3, '0')}. {word}  "
            line += phrase
            counter += 1
    return True


def contains(args):
    """
    Check if words exist that contain the partial word within the word.
    """
    if args.start or args.end:
        if args.start:
            return start(args)
        return end(args)
    else:
        output = []
        inp = sanatize(args.val)
        count = -1 if not count else int(count)
        for _, word in enumerate(Words.all_words):
            if count == 0:
                break
            if args.length and len(word) != int(args.length):
                continue
            if len([part for part in inp if part in word]) == len(inp):
                output.append(word)
                count -= 1
        if output:
            return show()
    return True


def start(args):
    """
    Check contains but only from the start of the word.
    """
    output = []
    inp = "".join(sanatize(args.val))
    count = -1 if not count else int(count)
    for _, word in enumerate(Words.all_words):
        if not count:
            break
        if args.length and len(word) != int(args.length):
            continue
        if word.startswith(inp):
            output.append(word)
            count -= 1
    if output:
        return show()
    return True


def end(args):
    """
    Check contains but only at the end of the word.
    """
    output = []
    inp = "".join(sanatize(args.val))
    count = -1 if not count else int(args.count)
    for _, word in enumerate(Words.all_words):
        if not count:
            break
        if args.length and len(word) != int(args.length):
            continue
        if word.endswith(inp) == len(inp):
            output.append(word)
            count -= 1
    if output:
        return show()
    return True


def binprint(args):
    """
    Return binary representation of decimal digit.
    """
    value = int(args.value)
    print(bin(value)[2:])
    return value


def mergesort(seq, word):
    if len(seq) <= 1:
        return seq
    left = mergesort(seq[: len(seq) // 2], word)
    right = mergesort(seq[len(seq) // 2 :], word)
    i = j = 0
    lst = []
    while i < len(left) and j < len(right):
        if len(left[i]) < len(right[j]):
            lst.append(left[i])
            i += 1
        elif len(left[i]) > len(right[j]):
            lst.append(right[j])
            j += 1
        elif left[i].index(word) < right[j].index(word):
            lst.append(left[i])
            i += 1
        else:
            lst.append(right[j])
            j += 1
    while i < len(left):
        lst.append(left[i])
        i += 1
    while j < len(right):
        lst.append(right[j])
        j += 1
    return lst


def synonyms(args):
    """
    Return Synonyms for the inputed word.
    """
    w = args.word.lower()
    precision = int(args.precision)
    collection = {}
    for entry in Words.synonyms:
        if w in entry["word"]:
            if entry["word"] in collection:
                collection[entry["word"]].extend(entry["synonyms"])
            else:
                collection[entry["word"]] = entry["synonyms"]
    lst = [w]
    if precision != 1:
        lst = mergesort(list(collection.keys()), w)
    m = min(len(lst), precision)
    for item in lst[:m]:
        output = f":{item} \n"
        prev = []
        for syn in collection[item]:
            if syn not in prev:
                prev.append(syn)
                output += f"\t {syn} \n"
        sys.stdout.write(output)
    return output


def wordle(args):
    size = int(args.size)
    print(args)
    print(size)
    if args.gui:
        start_gui()
    else:
        solve(l=size)


def utf(args):
    if args.numbers:
        for num in args.numbers:
            sys.stdout.write(chr(int(num)))
    elif args.range:
        for i in range(args.range[0], args.range[1]):
            sys.stdout.write(chr(i))
