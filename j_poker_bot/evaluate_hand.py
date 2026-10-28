# evaluate_hand.py

import random
from collections import Counter
from itertools import combinations

SUITS = ("hearts", "diamonds", "clubs", "spades")


def card_key(card):
    return (int(card["rank"]), card["suit"])


def score_five(cards):
    """Return a comparable score for exactly five cards."""
    ranks = sorted((card[0] for card in cards), reverse=True)
    counts = Counter(ranks)

    flush = len({card[1] for card in cards}) == 1

    unique = set(ranks)
    if 14 in unique:
        unique.add(1)  # Ace can be low in A-2-3-4-5

    straight = 0
    for high in range(14, 4, -1):
        if all(rank in unique for rank in range(high - 4, high + 1)):
            straight = high
            break

    groups = sorted(((count, rank) for rank, count in counts.items()), reverse=True)

    if flush and straight:
        return (8, straight)
    if groups[0][0] == 4:
        return (7, groups[0][1], groups[1][1])
    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, groups[0][1], groups[1][1])
    if flush:
        return (5, *ranks)
    if straight:
        return (4, straight)
    if groups[0][0] == 3:
        trips = groups[0][1]
        kickers = sorted((r for r in ranks if r != trips), reverse=True)
        return (3, trips, *kickers)
    if groups[0][0] == groups[1][0] == 2:
        pairs = sorted((groups[0][1], groups[1][1]), reverse=True)
        return (2, *pairs, groups[2][1])
    if groups[0][0] == 2:
        pair = groups[0][1]
        kickers = sorted((r for r in ranks if r != pair), reverse=True)
        return (1, pair, *kickers)

    return (0, *ranks)


def best_score(cards):
    """Find the strongest 5-card hand from 5 to 7 cards."""
    return max(score_five(hand) for hand in combinations(cards, 5))


def estimate_equity(hole_cards, community_cards, opponents=1, simulations=200):
    """
    Estimate showdown equity through random simulations.
    Ties receive a fractional share of the pot.
    """
    known = [card_key(c) for c in hole_cards + community_cards]

    if len(hole_cards) != 2 or len(known) != len(set(known)):
        raise ValueError("Invalid or duplicate known cards")

    deck = [
        (rank, suit)
        for suit in SUITS
        for rank in range(2, 15)
        if (rank, suit) not in known
    ]

    missing_board = 5 - len(community_cards)
    cards_needed = missing_board + 2 * opponents

    if missing_board < 0 or opponents < 1 or cards_needed > len(deck):
        raise ValueError("Invalid simulation parameters")

    equity = 0.0

    for _ in range(simulations):
        drawn = random.sample(deck, cards_needed)

        board = known[2:] + drawn[:missing_board]
        my_score = best_score(known[:2] + board)

        opponent_scores = []
        offset = missing_board

        for _ in range(opponents):
            opp_hole = drawn[offset : offset + 2]
            opponent_scores.append(best_score(opp_hole + board))
            offset += 2

        all_scores = [my_score] + opponent_scores
        best = max(all_scores)

        if my_score == best:
            equity += 1 / all_scores.count(best)

    return equity / simulations
