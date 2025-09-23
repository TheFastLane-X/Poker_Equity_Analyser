# src/monte_carlo.py
"""
Monte Carlo simulation for poker equity calculation.

Estimates win probability by simulating thousands of random outcomes.
"""

from typing import List, Tuple, Dict, Optional
import random
from .poker_engine import Card, Deck
from .hand_evaluator import HandEvaluator


class MonteCarloSimulator:
    """
    Calculate poker hand equity using Monte Carlo simulation.
    """
    
    @staticmethod
    def calculate_equity(
        player_cards: List[Card],
        community_cards: Optional[List[Card]] = None,
        num_opponents: int = 1,
        iterations: int = 10000
    ) -> Dict[str, float]:
        """
        Calculate win/tie/loss percentages for given cards.
        
        Parameters:
        player_cards : List[Card]
            Player's hole cards (2 cards)
        community_cards : List[Card], optional
            Community cards already dealt (0-5 cards)
        num_opponents : int, default=1
            Number of opponents
        iterations : int, default=10000
            Number of simulations to run
            
        Returns:
        Dict[str, float]
            {'win': 0.55, 'tie': 0.02, 'loss': 0.43}
            
        Example:
            AA vs 1 opponent pre-flop should return ~85% win
        """

        if community_cards is None:
            community_cards = []
        
        wins = 0
        ties = 0
        losses = 0
        
        for _ in range(iterations):
            # Create fresh deck
            deck = Deck()
            
            # Remove known cards (compare by rank and suit)
            remaining_cards = []
            for card in deck.cards:
                is_known = False
                for known_card in player_cards + community_cards:
                    if card.rank == known_card.rank and card.suit == known_card.suit:
                        is_known = True
                        break
                if not is_known:
                    remaining_cards.append(card)
            
            # Shuffle
            random.shuffle(remaining_cards)
            
            # Deal opponent hands
            opponent_hands = []
            cards_dealt = 0
            for i in range(num_opponents):
                opponent_hand = remaining_cards[cards_dealt:cards_dealt+2]
                opponent_hands.append(opponent_hand)
                cards_dealt += 2
            
            # Deal remaining community cards
            cards_needed = 5 - len(community_cards)
            new_community = remaining_cards[cards_dealt:cards_dealt+cards_needed]
            full_community = community_cards + new_community
            
            # Evaluate all hands
            player_eval = HandEvaluator.evaluate_hand(player_cards + full_community)
            
            # Check against all opponents
            player_wins = True
            player_ties = False
            
            for opp_hand in opponent_hands:
                opp_eval = HandEvaluator.evaluate_hand(opp_hand + full_community)
                result = HandEvaluator.compare_hands(player_eval, opp_eval)
                
                if result == -1:  # Player loses
                    player_wins = False
                    break
                elif result == 0:  # Tie
                    player_ties = True
                    player_wins = False
            
            if player_wins:
                wins += 1
            elif player_ties:
                ties += 1
            else:
                losses += 1
        
        results = {'win': wins / iterations, 'tie': ties / iterations, 'loss': losses / iterations}
        
        return results
            
    
    @staticmethod
    def calculate_range_equity(
        player_cards: List[Card],
        opponent_range: List[Tuple[Card, Card]],
        community_cards: Optional[List[Card]] = None,
        iterations_per_hand: int = 1000
    ) -> Dict[str, float]:
        """
        Calculate equity against specific opponent range.
        
        Parameters:
        player_cards : List[Card]
            Player's hole cards
        opponent_range : List[Tuple[Card, Card]]
            List of possible opponent hands
        community_cards : List[Card], optional
            Known community cards
        iterations_per_hand : int
            Iterations per opponent hand
            
        Returns:
        Dict[str, float]
            Equity percentages
        """

        if community_cards is None:
            community_cards = []
        
        wins = 0
        ties = 0
        losses = 0
        
        for opp_hand in opponent_range:
            # Check if this opponent hand conflicts with known cards
            opp_cards = list(opp_hand)  # Convert tuple to list
            
            # Skip if cards overlap
            conflicts = False
            for opp_card in opp_cards:
                for known_card in player_cards + community_cards:
                    if opp_card.rank == known_card.rank and opp_card.suit == known_card.suit:
                        conflicts = True
                        break
                if conflicts:
                    break
            
            if conflicts:
                continue
            
            # Run iterations for this specific opponent hand
            for _ in range(iterations_per_hand):
                deck = Deck()
                
                # Remove all known cards
                known_cards = player_cards + community_cards + opp_cards
                remaining_cards = []
                for card in deck.cards:
                    is_known = False
                    for known in known_cards:
                        if card.rank == known.rank and card.suit == known.suit:
                            is_known = True
                            break
                    if not is_known:
                        remaining_cards.append(card)
                
                random.shuffle(remaining_cards)
                
                # Deal remaining community
                cards_needed = 5 - len(community_cards)
                new_community = remaining_cards[:cards_needed]
                full_community = community_cards + new_community
                
                # Evaluate
                player_eval = HandEvaluator.evaluate_hand(player_cards + full_community)
                opp_eval = HandEvaluator.evaluate_hand(opp_cards + full_community)
                result = HandEvaluator.compare_hands(player_eval, opp_eval)
                
                if result == 1:
                    wins += 1
                elif result == 0:
                    ties += 1
                else:
                    losses +=1
        
        total = wins + ties + losses

        if total == 0:
            return {'win': 0.0, 'tie': 0.0, 'loss': 0.0}

        results = {'win': wins / total, 'tie': ties / total, 'loss': losses/ total}

        return results