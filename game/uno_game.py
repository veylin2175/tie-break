import random
from game.uno_card import UnoCard
from game.uno_player import UnoPlayer
from game.uno_com_player import UnoComPlayer
from game.uno_constants import COLORS, SPECIAL, WILD_SPECIAL, COLOR_ACTION_VALUES, WILD_ACTION_VALUES
from utils.timer import Timer
import time


# TODO: change com player hand to we can see the actual cards


class UnoGame:
    def __init__(self, players_info):
        self.deck = []
        self.players_info = players_info
        self.player_number = len(players_info)
        self.players = []
        self.com_players = []
        self.human_players = []
        self.discard_pile = []
        self.special_pile = []
        self.current_player_idx = 0
        self.next_player_idx = 1
        self.direction = 1
        self.game_over = False
        self.moving_card_nums = 0
        self.winner = None
        self.animation_infos = []
        self.selected_color = None
        self.top_color = None
        self.top_value = None
        self.game_event_infos = []
        self.uno_called_times = []
        self.turn_count = 0
        self.game_time = time.time()
        self.turn_timer = Timer()
        self.turn_ended = False
        self.human_turn_time, self.com_turn_time = 20, 2
        self.animation_finished = False
        self.part_card = None

        self._init_game()
        self._start_game()

    def _init_game(self):
        self._create_deck()
        UnoPlayer.init(self)
        self._add_players(self.players_info)

    # region Initializing Game Functions

    def _create_deck(self):
        """
        Creates a deck of cards
        """
        cards = []
        # Add color cards
        for color in COLORS:
            # Add color action cards
            for value in COLOR_ACTION_VALUES:
                cards.append(UnoCard(type="action", color=color, value=value))
            # Add wild cards
            for value in WILD_ACTION_VALUES:
                for _ in range(4):
                    cards.append(UnoCard(type="action", color="black", value=value))

        self.deck = cards

    def _shuffle_deck(self):
        random.shuffle(self.deck)

    def _recycle_discard_pile(self):
        self.deck = self.discard_pile[:-1]
        self._shuffle_deck()
        self.discard_pile = [self.discard_pile[-1]]

    # Deal 7 cards to each player in turns.
    def _deal_cards(self, num_cards=6):
        for i in range(num_cards):
            for player in self.players:
                self.add_card_move_animation(
                    card=self.deck.pop(0),
                    src="deck",
                    dest=f"player_{player.get_id()}",
                    delay=0.1,
                    duration=0.5,
                )

    # Add players to the game
    def _add_players(self, players_info):
        for i, player in enumerate(players_info):
            if player["is_com"]:
                self.players.append(UnoComPlayer(player["name"]))
            else:
                self.players.append(UnoPlayer(player["name"]))

        for player in self.players:
            if player.is_com():
                self.com_players.append(player)
            else:
                self.human_players.append(player)

    def _set_top_discard_card(self):
        self.add_card_move_animation(self.deck.pop(0), src="deck", dest="discard")

    # endregion

    # region get card
    def top_discard_card(self):
        return self.discard_pile[-1] if len(self.discard_pile) > 0 else None

    def _set_top_special_card(self):
        self.add_card_move_animation(self.deck.pop(0), src="deck", dest="discard")

    def top_special_card(self):
        return self.special_pile[-1] if len(self.special_pile) > 0 else None

    def top_deck_card(self):
        return self.deck[-1] if len(self.deck) > 0 else None

    # endregion

    # region set functions

    def set_animation_infos(self, animation_infos):
        self.animation_infos = animation_infos

    def set_game_event_infos(self, game_event_infos):
        self.game_event_infos = game_event_infos

    def set_selected_color(self, color):
        self.selected_color = color

    # endregion
    # region game play functions

    def draw_card(self, player, draw_number=1):
        for i in range(draw_number):
            if len(self.deck) == 0:
                self._recycle_discard_pile()
            if len(self.deck) == 0:
                return False
            card = self.deck.pop(0)
            self.add_card_move_animation(
                card, src="deck", dest=f"player_{player.get_id()}"
            )
        return True

    def can_play_card(self, card):
        if self.top_color == "black" or card.color == "black":
            return True
        if card.color == self.top_color or card.value == self.top_value:
            return True
        return False

    def play_card(self, player, card):
        if not self.can_play_card(card):
            return False
        player.play_card(card)
        if player.get_hand_size() == 1:
            player.set_is_uno(True)
            self.add_com_uno_called_times(player)
        self.add_card_move_animation(
            card, src=f"player_{player.get_id()}", dest="discard"
        )
        if card.type == "action":
            self._handle_action(player, card)

        return True

    # endregion

    def add_com_uno_called_times(self, player):
        for p in self.players:
            if p.is_com():
                if player == p:
                    random_time = random.uniform(0.5, 2)
                else:
                    random_time = random.uniform(1, 3)
                self.uno_called_times.append(
                    {"player": p, "time": self.game_time + random_time}
                )
        self.uno_called_times.sort(key=lambda x: x["time"])

    def uno_called(self, player):
        self.uno_called_times = []
        is_right_call = False
        for p in self.players:
            if p.get_is_uno() and p.get_uno_checked() == False:
                is_right_call = True
                p.set_uno_checked(True)
                if p != player:
                    p.set_uno_failed(True)

        if is_right_call:
            self.add_game_event_info("uno_called", player)
        return is_right_call

    # region Game Functions

    def _start_game(self):
        self._shuffle_deck()
        self._deal_cards()
        self._set_top_discard_card()
        self._start_turn(self.players[self.current_player_idx])

    def next_turn(self):
        self.next_player_idx += self.direction + self.player_number
        self.next_player_idx %= self.player_number

    def check_uno_failed(self, player):
        if player.get_uno_failed():
            self.draw_card(player)
            self.add_game_event_info("uno_failed", player)
            self.turn_ended = True

    def prev_turn(self):
        self.next_player_idx -= self.direction + self.player_number
        self.next_player_idx %= self.player_number

    def _start_turn(self, player):
        self.turn_timer.reset()
        player.turn_count += 1
        player.set_is_turn(True)
        if player.is_com():
            self.turn_timer.set_timer(self.com_turn_time)
        else:
            self.turn_timer.set_timer(self.human_turn_time)
        self.turn_timer.start()
        self.check_uno_failed(player)
        player.reset_uno_states()

    def process_game(self):
        if self.game_over:
            return
        self.game_time = time.time()
        self.process_uno()
        self.process_turn()

    def process_turn(self):
        if self.turn_timer.is_finished():
            self.turn_time_out(self.get_current_player())
        if self.animation_finished:
            self.turn_timer.resume()
        else:
            self.turn_timer.pause()
            return
        if self.turn_ended:
            self._end_turn(self.get_current_player())

    def process_uno(self):
        if len(self.uno_called_times) > 0:
            for uno_called_time in self.uno_called_times:
                if uno_called_time["time"] < self.game_time:
                    self.uno_called(uno_called_time["player"])
                    break

    # automatically play card, if player can't play, draw card
    def auto_turn(self, com_player):
        if not com_player.can_play(self.top_color, self.top_value):
            self.draw_card(com_player)
            return
        card = com_player.auto_card(self.top_color, self.top_value)
        self.play_card(com_player, card)

    def turn_time_out(self, player):
        if player.is_com():
            self.auto_turn(player)
        else:
            self.draw_card(player)
        self.turn_ended = True

    def _end_turn(self, player):
        self.turn_ended = False
        player.set_is_turn(False)
        if player.get_hand_size() == 0:
            self.add_game_event_info("player_win", player)
            self.game_over = True
            self.winner = self.get_current_player()
            somebody_uno = False
            for p in self.players:
                if p.uno_failed is False and p is not self.winner:
                    somebody_uno = True
                    break
            return

        self.turn_count += 1
        self._start_turn(self.get_next_player())
        self.current_player_idx = self.next_player_idx
        self.next_turn()

    # def uno(self, player):

    # endregion

    # region Card Functions

    def _handle_action(self, player, card):
        if card.value == "reverse":
            self.direction *= -1
            # change next player index
            self.next_player_idx += 2 * self.direction + self.player_number
            self.next_player_idx %= self.player_number
        elif card.value == "mistake":
            self.draw_card(self.get_next_player(), 2)
            self.next_turn()
        elif card.value == "unsportsmanlike_conduct":
            self.draw_card(self.get_next_player(), 4)
            self._change_color(player)
            self.next_turn()
        elif card.value == "challenge":
            self._change_color(player)

    # change color of top card to color which is most in player's hand
    def _change_color(self, player):
        if player.is_human():
            self.add_game_event_info("color_change_request", player.get_id())
            return
        color_count = {}
        for color in COLORS:
            color_count[color] = 0
        for card in player.hand:
            if card.color != "black":
                color_count[card.color] += 1
        self.selected_color = max(color_count, key=color_count.get)

    # endregion

    # # region Animation Functions
    def add_skip_animation(self, player, duration=1):
        player_idx = self.players.index(player)
        self.animation_infos.append(
            {
                "type": "skip",
                "player_idx": player_idx,
                "duration": duration,
            }
        )

    def add_card_move_animation(self, card, src, dest, delay=0.1, duration=0.5):
        self.animation_infos.append(
            {
                "type": "card_move",
                "card": card,
                "src": src,
                "dest": dest,
                "delay": delay,
                "duration": duration,
            }
        )
        self.moving_card_nums += 1
        if self.animation_finished:
            self.animation_finished = False

    def add_game_event_info(self, type, value):
        self.game_event_infos.append({"type": type, "value": value})

    def update_by_animation_info(self, info):
        if info["type"] == "card_move":
            card, dest = info["card"], info["dest"]
            if dest == "deck":
                self.deck.append(card)
            elif dest == "discard":
                self.discard_pile.append(card)
                self.part_card = str(card)
                self.part_card = self.part_card.split()
                if self.part_card[1] in WILD_SPECIAL:
                    self.special_pile.append(card)
                    self.part_card = None
                self.top_color = card.color
                self.top_value = card.value
                if card.value == "challenge" and self.selected_color is not None:
                    self.top_color = self.selected_color

            else:  # dest == "player_#"
                player_id = int(dest.split("_")[1])
                self.players[player_id].add_card(card)
            self.moving_card_nums -= 1

    # # endregion

    # region get functions
    def get_animation_infos(self):
        return self.animation_infos

    def get_game_event_infos(self):
        return self.game_event_infos

    def get_direction(self):
        return self.direction

    def get_com_players(self):
        return self.com_players

    def get_player(self, idx):
        return self.players[idx]

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def get_next_player(self):
        return self.players[self.next_player_idx]

    def get_remaining_turn_time(self):
        return self.turn_timer.get_remaining_time()

    def get_deck(self):
        return self.deck

    def get_top_color(self):
        return self.top_color

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner

    def set_turn_ended(self, ended):
        self.turn_ended = ended

    # endregion

    # region set functions
    def set_top_color(self, color):
        self.top_color = color

    def set_animation_finished(self, finished):
        self.animation_finished = finished