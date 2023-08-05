from dataclasses import dataclass
from typing import List, Tuple
from poker_game_runner.utils import HandType, card_num_to_str, get_hand_type, hand_str_to_enum

@dataclass(frozen=True)
class PlayerInfo: 
    """
        A class to represent the state of a player
    """
    spent: int
    """the amount the player has spent in this game"""
    stack: int
    """the amount the player has left"""
    active: bool
    """true if the player has not folded in this game"""

@dataclass(frozen=True)
class ActionInfo: 
    """
        A class to represent the action of a player
    """
    player: int
    """the index of the player taking this action"""
    action: int
    """the action of the player"""

    def __str__(self) -> str:
        player_str = "Player " + str(self.player) + ": "
        if self.action == 0:
            return player_str + "Fold"
        if self.action == 1:
            return player_str + "Call"
        return player_str + "Raise to " + str(self.action)

@dataclass(frozen=True)
class Observation: 
    """
    A class representing the state of the game
    
    """
    small_blind: int
    """The current small blind"""
    big_blind: int
    """The current big blind"""
    my_hand: Tuple[str]
    """The cards in the current players hand"""
    my_index: int
    """The index of the current player out of all players in the game"""
    board_cards: Tuple[str]
    """The community cards on the board"""
    player_infos: Tuple[PlayerInfo]
    """Current state of all players in the game"""
    history: Tuple[Tuple[ActionInfo]]
    """The history of all actions taken so far grouped by game round"""
    current_round: int
    """The current game round"""
    legal_actions: Tuple[int]
    """all legal actions"""

    def get_my_player_info(self):
        """ :return: the PlayerInfo of the current player  
            :rtype: PlayerInfo
        """
        return self.player_infos[self.my_index]

    def get_my_hand_type(self):
        """ :return: the hand type of the current player
            :rtype: HandType 
        """
        cards = self.my_hand + self.board_cards
        return get_hand_type(cards)
    
    def get_board_hand_type(self):
        """ :return: the hand type of the board cards 
            :rtype: HandType
        """
        if len(self.board_cards) == 0:
            return HandType.HIGHCARD
        return get_hand_type(self.board_cards)

    def get_player_count(self):
        """ :return: the number of players in the tournament 
            :rtype: int
        """
        return len(self.player_infos)

    def get_active_players(self):
        """ :return: the number of players that are active in the hand (have not folded) 
            :rtype: Tuple[PlayerInfo]
        """
        return tuple(p for p in self.player_infos if p.active)
    
    def get_actions_this_round(self):
        """ :return: the ActionInfo's from the current round 
            :rtype: Tuple[ActionInfo]
        """
        return self.get_actions_in_round(self.current_round)

    def get_actions_in_round(self, round_num: int):
        """ :return: the ActionInfo's from the given round
            :rtype: Tuple[ActionInfo]
            :type round_num: int
            :param round_num: the round to fetch actions from (0,1,2 or 3)
        """
        if round_num > 3 or round_num < 0:
            return tuple()
        return self.history[round_num]

    def get_max_spent(self):
        """ :return: the max spent from any player this game 
            :rtype: int
        """
        return max(map(lambda p: p.spent, self.player_infos))

    def get_call_size(self):
        """ :return: the amount to call 
            :rtype: int
        """
        return self.get_max_spent() - self.player_infos[self.my_index].spent

    def get_pot_size(self):
        """ :return: the amount in the pot
            :rtype: int
        """
        return sum(map(lambda p: p.spent, self.player_infos))
    
    def can_raise(self):
        """ :return: true if the current player can raise 
            :rtype: bool
        """
        return any(a for a in self.legal_actions if a > 1)
    
    def get_min_raise(self):
        """ :return: the minimum possible raise. Will return 1 (call) if the current player cannot raise
            :rtype: int
        """
        # Old method: return min(a for a in self.legal_actions if a > 1) if self.can_raise() else 1
        if self.can_raise():
            return next(val for val in self.legal_actions if val > 1)
        
        return 1

    def get_max_raise(self):
        """ :return: the maximum possible raise (all in). Will return 1 (call) if the current player cannot raise
            :rtype: int
        """
        # Old method: return max(a for a in self.legal_actions if a > 1) if self.can_raise() else 1
        if self.can_raise():
            return self.legal_actions[-1]
        
        return 1

    def get_fraction_pot_raise(self, frac):
        """ :return: the raise size in relation to the pot
            :rtype: int

            :type frac: float
            :param frac: The relative size of the pot to raise

        """
        if not self.can_raise():
            return 1
        else:
            pot = self.get_pot_size()
            call = self.get_call_size()
            pot_with_my_call = pot + call
            raise_amount = call + int(pot_with_my_call * frac)
            raise_to = self.get_my_player_info().spent + raise_amount
            if raise_to < self.get_min_raise():
                return self.get_min_raise()
            elif raise_to > self.get_max_raise():
                return self.get_max_raise()
            else:
                return raise_to


    def action_to_str(self, action_num: int, player_idx: int = None):
        if player_idx is None:
            player_idx = self.my_index
        if type(action_num) is not int or type(player_idx) is not int:
            return "unexpected types"
        return str(ActionInfo(player_idx, action_num))

class InfoState: 
    player_hands: Tuple[Tuple[str]]
    board_cards: List[str]
    player_infos: List[PlayerInfo]
    history: Tuple[List[ActionInfo]]
    small_blind: int
    big_blind: int
    current_round: int

    def __init__(self, history: List[int], stacks: List[int], blinds: List[int]):
        self.player_hands = tuple(
            tuple(
                map(card_num_to_str,
                    sorted(history[i:i+2], reverse=True)
                )
            )
            for i in range(0,len(history),2)
        )
        self.player_infos = [PlayerInfo(blind, stack-blind, True) for blind, stack in zip(blinds, stacks)]
        self.board_cards = []
        self.history = ([],[],[],[])
        self.small_blind = blinds[0]
        self.big_blind = blinds[1]
        self.current_round = 0

    def update_info_state_action(self, player_idx: int, action: int):
        player_info = self.player_infos[player_idx]
        if action > 1:
            r = action - player_info.spent
            self.player_infos[player_idx] = PlayerInfo(action, player_info.stack - r, player_info.active)
        elif action == 1:
            max_spent = max(map(lambda p: p.spent, self.player_infos))
            c = max_spent - player_info.spent
            self.player_infos[player_idx] = PlayerInfo(max_spent, player_info.stack - c, player_info.active)
        else:
            self.player_infos[player_idx] = PlayerInfo(player_info.spent, player_info.stack, False)
        self.history[self.current_round].append(ActionInfo(player_idx, action))


    def update_info_state_draw(self, card_num = int):
        cards_str = card_num_to_str(card_num)
        self.board_cards.append(cards_str)
        self.current_round = 0 if len(self.board_cards) < 3 else len(self.board_cards)-2
            
    def to_observation(self, player_idx: int, openspiel_legal_actions: List[int]):

        raise_actions = [action for action in self.history[self.current_round] if action.action > 1]
        if len(raise_actions) >= 5:
            legal_actions = [0,1] if 0 in openspiel_legal_actions else [1]
        else:
            legal_actions = openspiel_legal_actions

        assert legal_actions == sorted(legal_actions), "legal_actions from openspiel is always sorted"

        return Observation(
                        self.small_blind,
                        self.big_blind,
                        self.player_hands[player_idx], 
                        player_idx, 
                        tuple(self.board_cards), 
                        tuple(self.player_infos), 
                        tuple(tuple(h) for h in self.history),
                        self.current_round,
                        tuple(legal_actions))

