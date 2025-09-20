"""
Core poker components: Card, Deck, and basic logic
"""

from enum import IntEnum


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
    Represents a single playing card.
    
    Attributes:
        rank: Rank enum value (2-14)
        suit: Suit enum value (0-3)
    """

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        Initialise a card with rank and suit.
        
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
        String representation of card.
        
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
        Check if two cards are exactly the same.
        
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
        
        
