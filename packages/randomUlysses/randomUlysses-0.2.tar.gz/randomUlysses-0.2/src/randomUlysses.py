import random


def randomUlysses(offset: int):
    with open("./Ulysses.txt", "r") as f:

        text = f.read()

        i = random.randint(0, len(text))

        while(text[i] != ' '):
            i += 1
        start = i

        end = start + offset

        print(text[start:end + 1])
