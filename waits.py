#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass(frozen=True)
class Wait:
    pinfu: bool
    iipeiko: bool

    def __or__(self, other):
        return type(self)(self.pinfu or other.pinfu, self.iipeiko or other.iipeiko)

def add_wait(waitset, k, w):
    if k in waitset:
        waitset[k] |= w
    else:
        waitset[k] = w

@dataclass(frozen=True)
class State:
    location: int
    n1: int # ongoing length-1 runs
    n2: int # ongoing length-2 runs
    wait: bool # wait already used before
    pair: bool # pair already used before

    def score(self, hand):
        if self.location > len(hand):
            return {}
        if self.location == len(hand):
            if self.n2 > 0 or self.n1 > 1 or not self.pair:
                return {}
            if self.n1 == 0:
                if self.wait:
                    return {None: Wait(pinfu=True, iipeiko=False)}
                return {}
            # n1 == 1
            if self.wait:
                return {}
            return {self.location: Wait(pinfu=True, iipeiko=False)}
        waitset = {}
        for use_wait in {False, not self.wait}:
            for use_pair in {False, not self.pair}:
                if hand[self.location] + use_wait > 4:
                    continue
                leftover = hand[self.location] + use_wait - self.n1 - self.n2 - 2*use_pair
                if leftover < 0:
                    continue
                for use_set in {False, leftover >= 3}:
                    new_runs = leftover - 3*use_set
                    next_state = State(
                        location=self.location + 1,
                        n1=self.n2,
                        n2=new_runs,
                        wait=self.wait or use_wait,
                        pair=self.pair or use_pair,
                    )
                    next_waitset = yield next_state
                    for k, v in next_waitset.items():
                        new_k = self.location if use_wait else k
                        new_v = Wait(
                            pinfu=not use_set and v.pinfu and (not use_wait or self.n1 > 0 or new_runs > 0),
                            iipeiko=new_runs >= 2 or v.iipeiko,
                        )
                        add_wait(waitset, new_k, new_v)
        return waitset            

def dp(hand, already_used_wait=False, already_used_pair=False):
    outputs = {}
    stack = []

    state = State(location=0, n1=0, n2=0, wait=already_used_wait, pair=already_used_pair)
    gen = None
    ret = None
    while True:
        try:
            if gen is None:
                gen = state.score(hand)
                call = next(gen)
            else:
                call = gen.send(ret)
        except StopIteration as e:
            ret = e.value
            outputs[state] = ret
            if stack:
                (state, gen) = stack.pop()
                continue
            break
        if call in outputs:
            ret = outputs[call]
            continue
        stack.append((state, gen))
        state = call
        gen = None
        ret = None
    return ret

# hand is input as list of number of tiles, starting from 1; waits are returned starting from 0
def waits(hand, wait=True, pair=True):
    # renumber hand to start from 1, waits start from 0
    hand = [0] + list(hand) + [0]

    return dp(hand, not wait, not pair)

def main():
    while True:
        prompt = 'input hand> '
        hand = input(prompt)
        hand = [int(c) for c in hand]
        s = sum(hand)
        if s % 3 == 0:
            wait = pair = False
        elif s % 3 == 1:
            wait = True
            pair = True
        elif s % 3 == 2:
            wait = True
            pair = False
        w = waits([int(c) for c in hand], wait, pair)
        if wait:
            print(' ' * (len(prompt) - 1), end='')
            for i in range(len(hand) + 2):
                if i not in w:
                    c = ' '
                elif w[i].pinfu and w[i].iipeiko:
                    c = 'I'
                elif w[i].pinfu:
                    c = 'p'
                elif w[i].iipeiko:
                    c = 'i'
                else:
                    c = '^'
                print(c, end='')
            print()
        else:
            print(('OK' + (' PINFU' if w[None].pinfu else '') + (' IIPEIKO' if w[None].iipeiko else '')) if None in w else 'NO')

if __name__ == '__main__':
    main()
