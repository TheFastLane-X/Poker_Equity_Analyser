# src/hand_evaluator.py
"""
Poker hand evaluation and ranking system.

Identifies poker hands and determines winners in Texas Hold'em.
"""

from enum import IntEnum
from typing import List, Tuple, Optional
from collections import Counter
from .poker_engine import Card


class HandRank(IntEnum):
    """Poker hand rankings from lowest to highest."""
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


class HandEvaluator:
    """
    Evaluates poker hands and determines winners.
    
    Handles 5, 6, or 7 card hands (Texas Hold'em).
    """
    
    @staticmethod
    def evaluate_hand(cards: List['Card']) -> Tuple[HandRank, List[int]]:
        """
        Evaluate the best 5-card poker hand from given cards.
        
        Parameters:
        cards : List[Card]
            5-7 cards to evaluate
            
        Returns:
        Tuple[HandRank, List[int]]
            (hand_rank, tiebreakers)
            tiebreakers are ranks in descending order of importance
            
        Example:
            Full house KKK22 returns (HandRank.FULL_HOUSE, [13, 2])
            Flush A-K-Q-J-9 returns (HandRank.FLUSH, [14, 13, 12, 11, 9])
        """
        
        ranks = [int(card.rank) for card in cards]
        flush_ranks = HandEvaluator._check_flush(cards)
        straight_high = HandEvaluator._check_straight(ranks)
        fours, triples, pairs, kickers = HandEvaluator._check_pairs_and_sets(cards)
        
        # Royal flush
        if flush_ranks and straight_high == 14:
            # Need to verify it's actually A-K-Q-J-10 of same suit
            if set(flush_ranks) >= {14, 13, 12, 11, 10}:
                return (HandRank.ROYAL_FLUSH, [14])

        # Straight flush
        if flush_ranks and straight_high:
            # Check that it actually is a straight flush
            straight_flush = HandEvaluator._check_straight(flush_ranks)
            if straight_flush:
                return (HandRank.STRAIGHT_FLUSH, [straight_flush])
        
        # Four of a kind
        if fours:
            return (HandRank.FOUR_OF_A_KIND, fours + kickers[:1])
        
        # Full house
        if triples and pairs:
            return (HandRank.FULL_HOUSE, [triples[0], pairs[0]])
        elif len(triples) >= 2:
            return (HandRank.FULL_HOUSE, triples[:2])

        # Flush
        if flush_ranks:
            return (HandRank.FLUSH, flush_ranks)
        
        # Straights
        if straight_high:
            return (HandRank.STRAIGHT, [straight_high])
        
        # Three of a kind (Trips)
        if triples:
            return (HandRank.THREE_OF_A_KIND, triples + kickers[:2])
        
        # Two pair
        if len(pairs) >= 2:
            return (HandRank.TWO_PAIR, pairs[:2] + kickers[:1])
        
        # Pair
        if pairs:
            return (HandRank.PAIR, pairs + kickers[:3])

        # High card
        return (HandRank.HIGH_CARD, sorted(ranks, reverse=True)[:5])
    
    @staticmethod
    def _check_flush(cards: List['Card']) -> Optional[List[int]]:
        """
        Check if cards contain a flush.
        
        Parameters:
        cards : List[Card]
            Cards to check (need at least 5 of same suit)
            
        Returns:
        Optional[List[int]]
            Ranks of flush cards (highest 5) or None if no flush
        """

        suit_count = Counter(card.suit for card in cards)
        for suit, count in suit_count.items():
            if count >= 5:
                # Get all cards of this suit and return top 5 ranks
                flush_ranks = [int(card.rank) for card in cards if card.suit == suit]
                return sorted(flush_ranks, reverse=True)[:5]
    
        return None
                
    
    @staticmethod
    def _check_straight(ranks: List[int]) -> Optional[int]:
        """
        Check if ranks contain a straight.
        
        Parameters:
        ranks : List[int]
            Sorted unique ranks
            
        Returns:
        Optional[int]
            Highest rank in straight or None if no straight
            
        Note:
            Handle A-2-3-4-5 where Ace is low
        """
        # Remove duplicates and sort
        unique_ranks = sorted(set(ranks), reverse=True)
    
        # Check that there are enough ranks for a straight
        if len(unique_ranks) < 5:
            return None
        
        # Check for regular straights (5 consecutive ranks)
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                return unique_ranks[i]  # Return highest card in straight
    
        # Check for ace-low straight: A-2-3-4-5
        if set(unique_ranks) >= {14, 2, 3, 4, 5}:  # Ace is 14
            return 5  # In ace-low straight, 5 is the "high" card
    
        return None  # No straight found
    
    @staticmethod
    def _check_pairs_and_sets(cards: List['Card']) -> Tuple[List[int], List[int], List[int], List[int]]:
        """
        Find all pairs, three of a kinds, and four of a kinds.
        
        Parameters:
        cards : List[Card]
            Cards to analyse
            
        Returns:
        Tuple[List[int], List[int], List[int], List[int]]
            (fours, threes, pairs, kickers)
            Each list contains ranks sorted descending
        """
        
        rank_counts = Counter(card.rank for card in cards)

        fours = []
        triples = []
        pairs = []
        kickers = []

        for rank, count in rank_counts.items():
            if count == 4:
                fours.append(rank)
            elif count == 3:
                triples.append(rank)
            elif count == 2:
                pairs.append(rank)
            else:  # count == 1
                kickers.append(rank)

        return (sorted(fours, reverse=True), 
            sorted(triples, reverse=True),
            sorted(pairs, reverse=True),
            sorted(kickers, reverse=True))

    @staticmethod
    def compare_hands(hand1: Tuple[HandRank, List[int]], 
                     hand2: Tuple[HandRank, List[int]]) -> int:
        """
        Compare two evaluated hands.
        
        Parameters:

        hand1 : Tuple[HandRank, List[int]]
            First hand (rank, tiebreakers)
        hand2 : Tuple[HandRank, List[int]]
            Second hand (rank, tiebreakers)
            
        Returns:
        int
            1 if hand1 wins, -1 if hand2 wins, 0 if tie
        """
        # hand1 wins
        if hand1[0] > hand2[0]:
            return 1
        elif hand1[0] < hand2[0]:
            return -1
        
        # Same hand rank, compare tiebreakers t1 and t2
        for t1, t2 in zip(hand1[1], hand2[1]):
            if t1 > t2:
                return 1
            elif t1 < t2:
                return -1
            
        return 0

    @staticmethod
    def get_best_five_card_hand(cards: List['Card']) -> List['Card']:
        """
        Get the best 5-card hand from 5-7 cards.
        
        Parameters:
        cards : List[Card]
            5-7 cards to choose from
            
        Returns:
        List[Card]
            Best 5 cards that make the strongest hand
        """

        hand_rank, tiebreakers = HandEvaluator.evaluate_hand(cards)

        match hand_rank:
            case HandRank.ROYAL_FLUSH | HandRank.STRAIGHT_FLUSH:
                # Find flush suit
                suit_counts = Counter(card.suit for card in cards)
                flush_suit = None
                for suit, count in suit_counts.items():
                    if count >= 5:
                        flush_suit = suit
                        break
                
                # Get only cards of flush suit
                flush_cards = [card for card in cards if card.suit == flush_suit]
                
                # Now get the straight from these flush cards
                straight_flush_cards = HandEvaluator._get_straight_cards(flush_cards, tiebreakers[0])
                return straight_flush_cards
    
            case HandRank.FOUR_OF_A_KIND:
                # Get ranks for four of a kind and kicker
                quad_rank = tiebreakers[0]
                kicker_rank = tiebreakers[1]
                hand = []

                # Get all 4 cards for quad
                for card in cards:
                    if card.rank == quad_rank:
                        hand.append(card)
                
                # Get kicker
                for card in cards:
                     if card.rank == kicker_rank:
                        hand.append(card)
                        break
                     
                return hand
            
            case HandRank.FULL_HOUSE:
                # Get ranks for the full house
                triple_rank = tiebreakers[0]
                pair_rank = tiebreakers[1]
                hand = []

                for card in cards:
                    if card.rank == triple_rank:
                        hand.append(card)
                
                pair_count = 0
                for card in cards:
                    if card.rank == pair_rank:
                        hand.append(card)
                        pair_count += 1

                        if pair_count == 2:
                            break

                return hand

            case HandRank.FLUSH:
                # Find flush suit
                suit_counts = Counter(card.suit for card in cards)
                flush_suit = None
                for suit, count in suit_counts.items():
                    if count >= 5:
                        flush_suit = suit
                        break
                
                # Get all of cards of flush suit, sorted by rank
                flush_cards = [card for card in cards if card.suit == flush_suit]
                flush_cards = sorted(flush_cards, key=lambda card: card.rank, reverse=True)

                return flush_cards[:5]
                
            case HandRank.STRAIGHT:
                return HandEvaluator._get_straight_cards(cards, tiebreakers[0])
            
            case HandRank.THREE_OF_A_KIND:
                hand = []
                triple_rank = tiebreakers[0]
                kickers_ranks = tiebreakers[1:]
                for card in cards:
                     if card.rank == triple_rank:
                         hand.append(card)
                

                for card in cards:
                    if card.rank in kickers_ranks:
                        hand.append(card)
                    if len(hand) == 5:
                        break
            
                return hand
            
            case HandRank.TWO_PAIR:
                hand = []
                pair1_rank = tiebreakers[0]
                pair2_rank = tiebreakers[1]
                kicker_rank = tiebreakers[2]
                kicker_count = 0

                for card in cards:
                    if card.rank == pair1_rank:
                        hand.append(card)
                    elif card.rank == pair2_rank:
                        hand.append(card)
                    elif card.rank == kicker_rank and kicker_count == 0:
                        hand.append(card)
                        kicker_count += 1
                
                return hand
            
            case HandRank.PAIR:
                hand = []
                pair_rank = tiebreakers[0]
                kickers_rank = tiebreakers[1:]

                for card in cards:
                    if card.rank == pair_rank:
                        hand.append(card)
                    elif card.rank in kickers_rank:
                        hand.append(card)

                return hand
            
            case HandRank.HIGH_CARD:
                sorted_cards = sorted(cards, key=lambda x: x.rank, reverse=True)
                return sorted_cards[:5]

            case _:
                raise ValueError(f"Unhandled hand rank: {hand_rank}")


    @staticmethod
    def _get_straight_cards(cards: List['Card'], high_rank: int) -> List['Card']:
        """
        Get the cards that form a straight.

        Returns:
            List[Card]
                returns a list of cards that form a straight
        """
        
        if high_rank == 5:  # Wheel straight
            target_ranks = [14, 2, 3, 4, 5]
        else:
            target_ranks = list(range(high_rank - 4, high_rank + 1))
        
        # Now find cards matching these ranks
        straight_cards = []
        for rank in target_ranks:
            for card in cards:
                if card.rank == rank:
                    straight_cards.append(card)
                    break  # Only need one card of each rank
        
        return straight_cards
