# poker_ai.py

from evaluate_hand import estimate_equity


def choose_action(state, player_id):
    """Choose a legal basic action from the game state."""

    players = state["players"]

    me = next(player for player in players if player["id"] == player_id)

    hole_cards = me["hole_cards"]
    community_cards = state["community_cards"]

    # Ignore folded opponents
    active_opponents = [
        player
        for player in players
        if player["id"] != player_id
        and not player["folded"]
        and player["stack"] + player["bet"] >= 0
        and len(player["hole_cards"]) == 2
    ]

    opponent_count = len(active_opponents)

    if opponent_count == 0:
        return "check"

    # Estimate winning equity using Monte Carlo simulation
    equity = estimate_equity(
        hole_cards, community_cards, opponents=opponent_count, simulations=200
    )

    current_bet = max(player["bet"] for player in players)
    call_amount = max(0, current_bet - me["bet"])
    actual_call = min(call_amount, me["stack"])

    pot = state["pot"]

    # If no money is required, take the free card
    if call_amount == 0:
        action = "check"
        required_equity = 0.0
    else:
        required_equity = actual_call / (pot + actual_call)

        # Small safety margin for sampling uncertainty
        if equity >= required_equity + 0.05:
            action = "call"
        else:
            action = "fold"

    print(
        f"Phase={state['phase']} | "
        f"Equity={equity:.1%} | "
        f"Required={required_equity:.1%} | "
        f"Action={action}"
    )

    return action
