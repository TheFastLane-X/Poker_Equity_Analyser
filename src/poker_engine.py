"""
Core poker components: Card, Deck, and basic logic
"""

from enum import IntEnum
import random

class Rank(IntEnum):
    """Card ranks from 2 to Ace"""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(IntEnum):
    """Card suits in poker"""

    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


class Card():
    """
    Represents a single playing card
    
    Attributes:
        rank: Rank enum value (2-14)
        suit: Suit enum value (0-3)
    """

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        Initialise a card with rank and suit
        
        Args:
            rank: Rank enum (e.g., Rank.ACE)
            suit: Suit enum (e.g., Suit.SPADES)
        """

        self.rank = rank
        self.suit = suit

    def __repr__(self):
        """
        Representation of Card object

        Returns:
            str: String literal of Card object
        """
        return f"Card(Rank.{self.rank.name}, Suit.{self.suit.name})"

    def __str__(self) -> str:
        """
        String representation of card
        
        Returns:
            String like "A♠" or "K♥" or "7♣"    
        """
        rank_symbols = "23456789TJQKA"
        suit_symbols = "♥♦♣♠"

        rank_char = rank_symbols[self.rank - 2]
        suit_char = suit_symbols[self.suit]
        return f"{rank_char}{suit_char}"

    def __eq__(self, other: 'Card') -> bool:
        """
        Check if two cards are exactly the same
        
        Parameters:
            other : Card Another Card object
            
        Returns:
            bool: True if same rank AND suit
        """
        
        return self.rank == other.rank and self.suit == other.suit
        
    def __lt__(self, other: 'Card') -> bool:
        """
        Compare if card is less than other

        Args:
            other (Card): Another Card object

        Returns:
            bool: True if rank of card is less than other

        """

        return self.rank < other.rank
      

class Deck:
    """
    Standard 52 card deck for poker

    Attributes:
        cards: List of Card objects remaining in deck
    """

    def __init__(self) -> None:
        """
        Initialise a full 52 deck card and shuffle it
        """
        
        self.cards = [Card(rank, suit) for suit in Suit for rank in Rank]
        self.shuffle()
    
    def shuffle(self) -> None:
        """
        Shuffles deck randomly
        """
    
        random.shuffle(self.cards)
    
    def __str__(self):
        """
        String representation of deck

        Returns:
            str: Shows number of cards and first few cards
        """

        if not self.cards:
            return "Deck(empty)"
        
        cards_to_show = min(5, len(self.cards))
        card_str = ', '.join(str(card) for card in self.cards[:cards_to_show])

        if len(self.cards) > cards_to_show:
            return f"Deck ({len(self.cards)} cards): {card_str}, ..."
        else:
            return f"Deck ({len(self.cards)} cards): {card_str}"


    def deal(self) -> Card:
        """
        Deal a single card from the deck

        Returns:
            Card: The dealt card

        Raises:
            ValueError: if deck is empty
        """

        if not self.cards:
            raise ValueError("Cannot deal from an empty deck")
        
        return self.cards.pop()

    def deal_to_players(self, num_players: int, cards_per_player: int = 2) -> list[list[Card]]:
        """
        Deals cards to players one by one 
        Args:
            num_players (int): number of players to deal cards to
            cards_per_player (int, optional): Number of cards to deal to players. Defaults to 2.

        Returns:
            list[list[Card]]: Hands in position order
        """

        total_cards_needed = num_players * cards_per_player
        
        if total_cards_needed > len(self.cards):
            raise ValueError(f"Cannot deal {total_cards_needed}, as only {len(self.cards)} cards in the deck")
        
        hands = [[] for player in range(num_players)]
        
        for _ in range(cards_per_player):
            for player in range(num_players):
                hands[player].append(self.deal())

        return hands

    def deal_community_cards(self, num_cards: int) -> list[Card]:
        """
        Deals community cards (flop/turn/river)

        Args:
            num_cards (int): number of cards to deal

        Returns:
            list[Card]: list of community cards
        """
        return [self.deal() for _ in range(num_cards)]


def display_hands(hands: list[list[Card]]) -> None:
    """
    Displays hands of all players

    Args:
        hands (list[list[Card]]): List of player hands
    """

    for i, hand in enumerate(hands, 1):
        hand_str = ', '.join(str(card) for card in hand)
        print(f"Player {i}: [{hand_str}]")
