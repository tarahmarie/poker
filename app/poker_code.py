# -*- coding: utf-8 -*-

import json
from collections import Counter

TEN = 10
JACK = 11
QUEEN = 12
KING = 13
ACE = 14
WHEEL = set([2, 3, 4, 5, 14])
STRAIGHT_FLUSH = 9
QUADS = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
SET = 4
TWO_PAIR = 3
PAIR = 2
HIGH_CARD = 1

def value_tie_breaker(hand, kind):
    checker = list()
    hand_list = hand_value(hand, False)
    for index in range(len(hand_list)):
        checker.append(hand_list[index])
    c = Counter(checker)
    list_c = list()
    for index in range(len(c)):
        a = c.items()[index][0]
        b = c.items()[index][1]
        value_pair = (a, b)
        list_c.append(value_pair)
    ol = sorted(list_c, key=lambda x: (x[1], x[0]), reverse=True)
    print "Ordered List is %s " % ol
    if (kind == FLUSH) or (kind == HIGH_CARD):
        elements = (ol[0], ol[1], ol[2], ol[3], ol[4])
    elif kind == PAIR:
        elements = (ol[0], ol[1], ol[2], ol[3])
    elif (kind == TWO_PAIR) or (kind == SET):
        elements = (ol[0], ol[1], ol[2])
    elif (kind == QUADS) or (kind == FULL_HOUSE):
                elements = (ol[0], ol[1])

    return elements


def winner(h1, h2, h1e, h2e, p1, p2):
    """
    Returns the winning hand between P1 and P2. If tie, a print msg tie will pop.
    Passing in hands, their evaluation, and the players.
    :return: p1 or p2

    >>>
    """
    winning_player = "Nobody"
    winning = max(h1e, h2e)
    if h1e == h2e:
        breakATie = tiebreaker(h1, h1e, h2, h2e)
        print "The winner is %s" % breakATie
        winning_player = breakATie
    else:

        if winning == h1e:
            winning_player = p1
        else:
            winning_player = p2

    print "The winner is %s with a %s." % (winning_player, winning)

    return winning_player


def tiebreaker(h1, h1e, h2, h2e):
    winner = "Nobody"
    list1 = hand_value(h1, False)
    list2 = hand_value(h2, False)

    if (h1e == STRAIGHT_FLUSH and h2e == STRAIGHT_FLUSH) or (h1e == STRAIGHT and h2e == STRAIGHT):
        if max(list1) > max(list2):
            winner = "Player1"
        elif max(list2) > max(list1):
            winner = "Player 2"
        else:
            winner = "It's a tie."
    elif (h1e == h2e):
        print "testing tie method"
        value1 = value_tie_breaker(h1, h1e)
        value2 = value_tie_breaker(h2, h2e)
        p1 = "Player 1"
        p2 = "Player 2"
        tie = "It's a tie"
        if value1[0] > value2[0]:
            winner = p1
        elif value2[0] > value1[0]:
            winner = p2
        elif value1[0] == value2[0]:
            if value1[1] > value2[1]:
                winner = p1
            elif value2[1] > value1[1]:
                winner = p2
            elif value1[1] == value2[1]:
                if value1[2] > value2[2]:
                    winner = p1
                elif value2[2] > value1[2]:
                    winner = p2
                elif value1[2] == value2[2]:
                    if value1[3] > value2[3]:
                        winner = p1
                    elif value2[3] > value1[3]:
                        winner = p2
                    elif value1[3] == value2[3]:
                        winner = p1
                        if value1[4] > value2[4]:
                            winner = p1
                        elif value2[4] > value1[4]:
                            winner = p2
                        elif value1[4] == value2[4]:
                            winner = tie

    return winner


def evaluate(hand):
    try:
        fr = flush_finder(hand)
        sr = straight_finder(hand)
        if fr == 1 and sr == 1:
            result = STRAIGHT_FLUSH
        elif fr == 1 and sr != 1:
            result = FLUSH
        elif sr == 1 and fr != 1:
            result = STRAIGHT
        else:
            result = hand_valuation(hand)
    except:
        raise Exception("BAAAAAD")

    return result


def hand_valuation(hand):
    result = 0
    num_unique = len(hand_value(hand))
    if num_unique == 2 or num_unique == 3:
        result = quad_fh_set_and_two_pair_finder(hand)
    elif num_unique == 4:
        result = PAIR
    elif num_unique == 5:
        result = HIGH_CARD

    return result


def quad_fh_set_and_two_pair_finder(hand):
    checker = list()
    for index in range(len(hand)):
        checker.append(hand[index][0])
    c = Counter(checker)
    e1 = c.items()[0][1]
    e2 = c.items()[1][1]
    e3 = c.items()[2][1]
    if e1 == 3 or e2 == 3 or e3 == 3:
        kind = SET
    elif e1 == 2 or e2 == 2 or e3 == 2:
        kind = TWO_PAIR
    elif e1 == 4 or e2 == 4:
        kind = QUADS
    elif (e1 == 3 and e2 == 2) or (e1 ==2 and e2 == 3):
        kind = FULL_HOUSE

    return kind


def parse_json(filename='data.json'):
    with open(filename) as data_file:
        data = json.load(data_file)

    return data


def flush_finder(hand):
    is_flush = 0
    suits = set([])
    for index in range(len(hand)):
        suits.add(hand[index][1])
    if len(suits) == 1:
        is_flush = 1

    return is_flush


def straight_finder(hand):
    is_straight = 0
    values = hand_value(hand, True)
    topCard = max(values)
    bottomCard = min(values)
    if values == WHEEL:
        print "You have a wheel and this is a weird and special case."
        is_straight = 1
    elif values != WHEEL and len(values) == 5:
        if topCard - bottomCard == 4:
            is_straight = 1

    return is_straight


def hand_value(hand, is_set):
    set_value = set([])
    list_value = list()
    for index in range(len(hand)):
        v = hand[index][0]
        if v == "T":
            int_v = TEN
        elif v == "J":
            int_v = JACK
        elif v == "Q":
            int_v = QUEEN
        elif v == "K":
            int_v = KING
        elif v == "A":
            int_v = ACE
        else:
            int_v = int(v)

        if is_set == True:
            set_value.add(int_v)
        else:
            list_value.append(int_v)

    if is_set == True:
        values = set_value
    else:
        values = list_value

    return values


def web_server():
    """
    This method is for web server access to the code.

    :return: a string message of who the winner is.

    >>> import poker_code
    >>> poker_code.web_server()
    The winner is Player1
    The winner is Player1 with a 5.
    'Player1'
    """
    data = parse_json()
    p1 = data["hands"][0]["name"]
    p2 = data["hands"][1]["name"]
    h1 = data["hands"][0]["hand"]
    h2 = data["hands"][1]["hand"]
    h1e = evaluate(h1)
    h2e = evaluate(h2)

    msg = winner(h1, h2, h1e, h2e, p1, p2)
    return msg


if "__main__" == __name__:
    data = parse_json()
    p1 = data["hands"][0]["name"]
    p2 = data["hands"][1]["name"]
    h1 = data["hands"][0]["hand"]
    h2 = data["hands"][1]["hand"]
    h1e = evaluate(h1)
    h2e = evaluate(h2)

    winner(h1, h2, h1e, h2e, p1, p2)


