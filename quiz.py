#!/usr/bin/env python3

from waits import waits
from random import shuffle, randrange, choice

def random_hand(n):
    width = randrange((n + 2)//3, min(n, 9))
    hand = {x: 1 for x in range(width)}
    for _ in range(n - width):
        z = choice([x for (x, v) in hand.items() if v < 4])
        hand[z] += 1

    hand = [x for (x, v) in hand.items() for _ in range(v)]
    hand.sort()
    start = randrange(1, 9-width+2)
    return [x + start for x in hand]

def tanki_waits(hand):
    l = [hand.count(i) for i in range(1, 10)]
    return {k: v for k, v in waits(l).items() if 1 <= k <= 9}

def shanpon_waits(hand):
    l = [hand.count(i) for i in range(1, 10)] + [0, 0, 2]
    return {('N' if k == 12 else k): v for k, v in waits(l).items() if 1 <= k <= 9 or k == 12}

def quiz(s):
    hand = random_hand(s)
    sh = ''.join(str(x) for x in hand)
    if s % 3 == 0:
        raise ValueError
    elif s % 3 == 1:
        extra = ''
        if len(hand) < 13:
            extra = ''.join([' EEE', ' SSS', ' WWW'][:(13 - len(hand))//3])
        ans = input(f'{sh}{extra}> ')
    elif s % 3 == 2:
        extra = ''
        if len(hand) < 11:
            extra = ''.join([' EEE', ' SSS', ' WWW'][:(11 - len(hand))//3])
        ans = input(f'{sh}{extra} NN> ')
    if s % 3 == 1:
        w = set(tanki_waits(hand))
    elif s % 3 == 2:
        w = set(shanpon_waits(hand))
    w = {str(x) for x in w}
    aset = set(ans.upper())
    if aset == w:
        print('correct')
    else:
        correct = ''.join(sorted(str(x) for x in w))
        print(f'incorrect: {correct}')

def main():
    while True:
        quiz(7)

if __name__ == '__main__':
    main()
