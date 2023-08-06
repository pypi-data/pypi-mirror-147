from time import time
from random import choice
import pyspiel
from poker_game_runner.state import InfoState, card_num_to_str
from poker_game_runner.utils import get_hand_type
from typing import List, Tuple
from collections import namedtuple
import eval7

BlindScheduleElement = namedtuple('BlindScheduleElement', 'next_blind_change small_blind big_blind ante')
Player = namedtuple('Player', 'bot_impl stack id')
ROUNDS = ['Preflop', 'Flop', 'Turn', 'River']

def play_tournament_table(bots, start_stack: int, use_timeout=True, console_output = False, calc_win_chance=False):
    
    json_data = []
    defeated_players = []
    hand_count = 0
    active_players = [Player(bot,start_stack, idx) for idx, bot in enumerate(bots)]
    blind_schedule = get_blind_schedule()
    blinds_iter = iter(blind_schedule)

    current_blinds = next(blinds_iter)
    while len(active_players) > 1:

        json_hand = {
            "hand_count": hand_count,
            "active_players": [player_to_dict(player) for player in active_players],
            "defeated_players": defeated_players
        }
        if console_output:
            print()
            print("----------------------------------------------------------")
            print("hand num: " + str(hand_count))
            print("Players in hand: ")
            [print(player.bot_impl.get_name() + " stack: " + str(player.stack)) for player in active_players]

        rewards, json_hand_events = play_hand(active_players, get_blinds_input(current_blinds, len(active_players)), use_timeout, console_output, calc_win_chance)
        json_hand["hand_events"] = json_hand_events

        if hand_count == current_blinds.next_blind_change:
            current_blinds = next(blinds_iter)
            
        newly_defeated_players, active_players = update_active_players(active_players, rewards, current_blinds.big_blind)

        defeated_players = defeated_players + newly_defeated_players
        active_players = active_players[1:] + [active_players[0]]
        hand_count += 1
        json_data.append(json_hand)
    
    results = defeated_players + [player_to_dict(active_players[0])]
    results.reverse()
    return results, json_data

def player_to_dict(player: Player, defeated = False):
    return {"name": player.bot_impl.get_name(), "id": player.id, "stack": player.stack if not defeated else 0}

def update_active_players(active_players: List[Player], rewards: List[int], big_blind: int):    
    updated_players = [Player(player.bot_impl, int(player.stack+r), player.id) for player,r in zip(active_players, rewards)]

    defeated_players = [player_to_dict(player, True) for player in updated_players if player.stack < big_blind]
    active_players = [player for player in updated_players if player.stack >= big_blind]
    return defeated_players, active_players

def get_blinds_input(current_blinds: BlindScheduleElement, playerCount: int) -> List[int]:
    return [current_blinds.small_blind, current_blinds.big_blind] + ([current_blinds.ante] * (playerCount-2))



def play_hand(players: List[Player], blinds: List[int], use_timeut, console_output=False, calc_win_chance=False):
    state, info_state, json_events = init_game(players, blinds, console_output)
    if console_output:
        print()
        print("-- betting round: " + ROUNDS[info_state.current_round] + " --")

    while not state.is_terminal():
        if state.is_chance_node():
            deck_cards = state.legal_actions()
            card_num = choice(deck_cards)
            apply_chance_action(state, info_state, json_events, card_num)
            deck_cards.remove(card_num)
            if len(info_state.board_cards) >= 3:
                
                if console_output:
                    print()
                    print("-- betting round: " + ROUNDS[info_state.current_round] + " --")
                    print("board: " + str(info_state.board_cards))
                if calc_win_chance:
                    add_win_chance_to_json(info_state, json_events, deck_cards)
            continue

        current_idx = state.current_player()
        action = get_player_action(players[current_idx], state, info_state, current_idx, use_timeut, console_output)
        apply_player_action(state, info_state, json_events, current_idx, action)
        if console_output:
            name = players[current_idx].bot_impl.get_name()
            if action == 0:
                print(name + " fold")
            elif action == 1:
                print(name + " call")
            else:
                print(name + " raise to " + str(action))
    
    json_events = json_events + [{
        "type": "reward", 
        "player": i, 
        "reward": reward, 
        "handtype": get_hand_type(list(info_state.board_cards) + list(info_state.player_hands[i])).name
    } for i, reward in enumerate(state.rewards())]
    if console_output:
        print()
        for i, reward in enumerate(state.rewards()):
            name = name = players[i].bot_impl.get_name()
            hand = str(info_state.player_hands[i])
            if info_state.player_infos[i].active:
                print_str = name + hand + (" won " if reward >= 0 else " lost ") + str(reward)
                if len(info_state.board_cards) == 5:
                    print_str += " with a " + get_hand_type(list(info_state.board_cards) + list(info_state.player_hands[i])).name
                print(print_str)
            else:    
                print(name + hand + " lost " + str(reward) + " after folding")

    return list(map(int, state.rewards())), json_events

def get_player_action(player, state, info_state: InfoState, current_idx: int, use_timeout: bool, console_output: bool):
    observation = info_state.to_observation(current_idx, state.legal_actions())
    try:
        action = get_player_action_with_timeout(player, observation, 1 if use_timeout else 1000000)
    except BaseException as e:
        if console_output:
            print(f"Bot: '{player.bot_impl.get_name()}' caused an exception!!! Folding on their behalf.")
            print(e)
        action = 0
    if not (action in observation.legal_actions and action in state.legal_actions()):
        if console_output:
            print(f"Bot: '{player.bot_impl.get_name()}' took action '{action}' which is illigal")
        if 0 in state.legal_actions() and 0 in observation.legal_actions:
            action = 0
        else:
            action = 1
    return action

def get_player_action_with_timeout(player, obs, timeout):
    start = time()
    res = player.bot_impl.act(obs)
    end = time()
    delta = end - start
    if delta > timeout:
        print(f"Bot: '{player.bot_impl.get_name()}' took too long to return. Folding on their behalf.")
        return 0
    return res

def run_act_on_bot(bot, obs, pipe):
    pipe.send(bot.act(obs))


def apply_player_action(state, info_state, json_events, current_idx, action):
    state.apply_action(action)
    info_state.update_info_state_action(current_idx, action)
    json_events.append({"type": "action", "player": current_idx, "action": int(action)})

def apply_chance_action(state, info_state, json_events, card_num):
    state.apply_action(card_num)
    info_state.update_info_state_draw(card_num)
    json_events.append({"type": "deal", "player": -1, "action": card_num_to_str(card_num)})

def add_win_chance_to_json(info_state: InfoState, json_events, deck_cards):
    active_idxs = {i: 0 for i, player in enumerate(info_state.player_infos) if player.active}

    sample_count = 0
    if len(info_state.board_cards) == 5:
        sample_count += 1
        winner_idx = get_winner_index(info_state, active_idxs, info_state.board_cards)
        if not winner_idx == -1:
            active_idxs[winner_idx] += 1
    elif len(info_state.board_cards) == 4:
        for i in range(len(deck_cards)):
            sample_count += 1
            board_cards = list(info_state.board_cards)
            board_cards.append(card_num_to_str(deck_cards[i]))
            winner_idx = get_winner_index(info_state, active_idxs, board_cards)
            if not winner_idx == -1:
                active_idxs[winner_idx] += 1
    elif len(info_state.board_cards) == 3:
        for i in range(len(deck_cards)-1):
            for j in range(i+1, len(deck_cards)):
                sample_count += 1
                board_cards = list(info_state.board_cards)
                board_cards.append(card_num_to_str(deck_cards[i]))
                board_cards.append(card_num_to_str(deck_cards[j]))
                winner_idx = get_winner_index(info_state, active_idxs, board_cards)
                if not winner_idx == -1:
                    active_idxs[winner_idx] += 1

    for i in active_idxs:
        wins = active_idxs[i]
        win_chance = wins / sample_count
        json_events.append({"type": "win_chance", "player": i, "win_chance": win_chance})

def get_winner_index(info_state, active_idxs, board_cards):
    evals = {}
    for i in active_idxs:
        hand = list(info_state.player_hands[i])
        evalCards = list(map(eval7.Card, board_cards + hand))
        eval = eval7.evaluate(evalCards)
        evals[i] = eval #.append((eval, i))
    max_val = max(evals.values())
    winnerCount = list(evals.values()).count(max_val)
    if (winnerCount) > 1:
        return -1
    return max(evals, key=evals.get)


def init_game(players: List[Player], blinds, console_output):
    game = pyspiel.load_game("universal_poker", {
        "betting": "nolimit",
        "bettingAbstraction": "fullgame",
        "numPlayers": len(players),
        "stack": " ".join(str(player.stack) for player in players),
        "blind": " ".join(str(blind) for blind in blinds),
        "numRounds": 4,
        "numHoleCards": 2,
        "numBoardCards": "0 3 1 1",
        "numSuits": 4,
        "numRanks": 13,
        "firstPlayer": "3 1 1 1" if len(players) > 2 else "1 1 1 1"
    })

    state = game.new_initial_state()

    #deal private cards
    while state.is_chance_node():
        state.apply_action(choice(state.legal_actions()))
        continue

    info_state = InfoState(state.history(), [p.stack for p in players], [b for b in blinds])
    json_events = []
    json_events.append({"type": "action", "player": 0, "action": blinds[0]})
    json_events.append({"type": "action", "player": 1, "action": blinds[1]})
    cards = [card_num_to_str(c) for c in state.history()]
    json_events = json_events + [{"type": "deal", "player": int(i/2), "card": card} for i, card in enumerate(cards)]

    if console_output:
        print()
        print(players[0].bot_impl.get_name() + " is small blind for " + str(blinds[0]))
        print(players[1].bot_impl.get_name() + " is big blind for " + str(blinds[1]))
        [print(players[int(i/2)].bot_impl.get_name() + " hand: " + cards[i] + cards[i+1]) for i in range(0, len(cards), 2)]
    return state, info_state, json_events

def get_blind_schedule():
    return (BlindScheduleElement(20, 10,20,0),     
            BlindScheduleElement(40, 15,30,0),
            BlindScheduleElement(60, 20,40,0),
            BlindScheduleElement(80, 25,50,0),
            BlindScheduleElement(100, 30,60,0),
            BlindScheduleElement(120, 40,80,0),
            BlindScheduleElement(140, 55,110,0),
            BlindScheduleElement(160, 75,150,0),
            BlindScheduleElement(180, 100,200,0),
            BlindScheduleElement(200, 130,260,0),
            BlindScheduleElement(220, 165,330,0),
            BlindScheduleElement(240, 205,410,0),
            BlindScheduleElement(260, 250,500,0),
            BlindScheduleElement(280, 300,600,0),
            BlindScheduleElement(300, 375,750,0),
            BlindScheduleElement(320, 500,1000,0),
            BlindScheduleElement(340, 750,1500,0),
            BlindScheduleElement(360, 1000,2000,0),
            BlindScheduleElement(380, 1500,3000,0),
            BlindScheduleElement(-1, 2500,5000,0))