"""
Poker strategy calculations: pot odds, EV, and decision making.

Provides mathematical framework for optimal poker decisions.
"""

from typing import Dict, Optional, Any
from .monte_carlo import MonteCarloSimulator
from .poker_engine import Card


class StrategyCalculator:
    """
    Calculate pot odds and expected value for poker decisions.
    """
    
    @staticmethod
    def calculate_pot_odds(pot_size: float, call_amount: float) -> float:
        """
        Calculate pot odds as a percentage.
        
        Parameters:
        pot_size : float
            Current size of the pot
        call_amount : float
            Amount required to call
            
        Returns:
        float
            Pot odds as a decimal (0.25 = 25%)
            
        Example:
            Pot: $100, Call: $25
            Pot odds = 25 / (100 + 25) = 0.20 = 20%
        """

        pot_odds = call_amount / (pot_size + call_amount)
        
        return pot_odds
    
    @staticmethod
    def calculate_ev(equity: float, pot_size: float, call_amount: float) -> float:
        """
        Calculate expected value of a call.
        
        Parameters:
        equity : float
            Win/Tie probability (from Monte Carlo)
        pot_size : float
            Current pot size
        call_amount : float
            Amount to call
            
        Returns:
        float
            Expected value (positive = profitable, negative = unprofitable)
            
        Example:
            55% equity, $100 pot, $25 call
            EV = (0.55 * $125) - (0.45 * $25) = $57.50
        """

        total_pot = pot_size + call_amount
        loss_pct = 1-equity

        # EV = (win% * win amount) - (loss% * loss amount)
        ev = (equity * total_pot) - (loss_pct * call_amount)
        
        return ev
    
    @staticmethod
    def calculate_breakeven_equity(pot_size: float, call_amount: float) -> float:
        """Calculate minimum equity needed to break even (equals pot odds)."""
        return StrategyCalculator.calculate_pot_odds(pot_size, call_amount)
    
    @staticmethod
    def get_decision(
        player_cards: list[Card],
        community_cards: Optional[list[Card]],
        pot_size: float,
        call_amount: float,
        num_opponents: int = 1,
        iterations: int = 10000
    ) -> Dict[str, Any]:
        """
        Get recommended action based on equity vs pot odds.
        
        Parameters:
        player_cards : list[Card]
            Player's hole cards
        community_cards : list[Card], optional
            Community cards on board
        pot_size : float
            Current pot size
        call_amount : float
            Amount to call (0 if checking)
        num_opponents : int
            Number of active opponents
        iterations : int
            Monte Carlo iterations
            
        Returns:
        Dict containing:
            - 'action': 'call', 'fold', or 'check'
            - 'equity': calculated win probability
            - 'pot_odds': required equity to break even
            - 'ev': expected value
            - 'profitable': boolean
            
        Example:
            {'action': 'call', 'equity': 0.55, 'pot_odds': 0.20, 
             'ev': 57.50, 'profitable': True}
        """
       
        MC_results = MonteCarloSimulator.calculate_equity(player_cards, community_cards, num_opponents, iterations)
        equity = MC_results['win'] + (MC_results['tie'] / 2)
        pot_odds = StrategyCalculator.calculate_pot_odds(pot_size, call_amount)
        ev = StrategyCalculator.calculate_ev(equity, pot_size, call_amount)
       
        if call_amount == 0:
            action = 'check'
        elif ev > 0:
            action = 'call'
        else:
            action = 'fold'
       
        return{'action': action,
                'equity': equity,
                'pot_odds': pot_odds,
                'ev': ev,
                'profitable' : ev > 0
        }