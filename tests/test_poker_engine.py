# tests/test_poker_engine.py
"""
Basic tests for poker engine functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.poker_engine import Card, Deck, Rank, Suit
from src.hand_evaluator import HandEvaluator, HandRank
from src.monte_carlo import MonteCarloSimulator


def test_card_creation():
    """Test card creation and display."""
    print("\n=== Testing Card Creation ===")
    ace_spades = Card(Rank.ACE, Suit.SPADES)
    print(f"Created card: {ace_spades}")
    print(f"Repr: {repr(ace_spades)}")
    assert ace_spades.rank == Rank.ACE
    assert ace_spades.suit == Suit.SPADES
    print("Card creation works")


def test_deck_dealing():
    """Test deck functionality."""
    print("\n=== Testing Deck ===")
    deck = Deck()
    print(f"Deck size: {len(deck.cards)}")
    
    hands = deck.deal_to_players(2, 2)
    # Pretty print the hands
    for i, hand in enumerate(hands, 1):
        hand_str = ', '.join(str(card) for card in hand)
        print(f"Player {i}: {hand_str}")
    
    assert len(deck.cards) == 48
    print("Deck dealing works")


def test_hand_evaluation():
    """Test hand evaluator with known hands."""
    print("\n=== Testing Hand Evaluation ===")
    
    # Royal flush
    royal = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.THREE, Suit.DIAMONDS)
    ]
    
    result = HandEvaluator.evaluate_hand(royal)
    print(f"Royal flush evaluation: {result}")
    assert result[0] == HandRank.ROYAL_FLUSH
    print("Royal flush detected")
    
    # Pair
    pair = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.DIAMONDS)
    ]
    
    result = HandEvaluator.evaluate_hand(pair)
    print(f"Pair evaluation: {result}")
    assert result[0] == HandRank.PAIR
    print("Pair detected")


def test_monte_carlo():
    """Test Monte Carlo simulation."""
    print("\n=== Testing Monte Carlo ===")
    
    # AA vs random
    pocket_aces = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.HEARTS)
    ]
    
    print("Running 10,000 simulations for AA vs 1 opponent...")
    results = MonteCarloSimulator.calculate_equity(
        pocket_aces, 
        community_cards=None,
        num_opponents=1,
        iterations=10000
    )
    
    print(f"Results: Win={results['win']:.2%}, Tie={results['tie']:.2%}, Loss={results['loss']:.2%}")
    
    # AA should win ~85% vs random hand
    assert results['win'] > 0.75  # Should be around 0.85
    print("Monte Carlo simulation works")


def test_monte_carlo_with_timing():
    """Test Monte Carlo simulation with performance measurement."""
    print("\n=== Testing Monte Carlo with Timing ===")
    
    # AA vs random
    pocket_aces = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.HEARTS)
    ]
    
    print("\nRunning simulation with timing enabled...")
    results = MonteCarloSimulator.calculate_equity(
        pocket_aces, 
        community_cards=None,
        num_opponents=1,
        iterations=10000,
        measure_time=True  # Enable timing
    )
    
    print(f"Results: Win={results['win']:.2%}, Tie={results['tie']:.2%}, Loss={results['loss']:.2%}")
    print(f"Time taken: {results['time_seconds']:.3f} seconds")
    print(f"Performance: {results['iterations_per_second']:.0f} iterations/second")
    
    # Verify timing data exists
    assert 'time_seconds' in results
    assert 'iterations_per_second' in results
    assert results['iterations_per_second'] > 0
    print("Timing metrics work correctly")
    
    # Performance scaling test
    print("\n=== Performance Scaling Test ===")
    print("Iterations | Time (s) | Iter/sec")
    print("-" * 35)
    
    for iterations in [1000, 5000, 10000, 25000]:
        results = MonteCarloSimulator.calculate_equity(
            pocket_aces,
            num_opponents=1,
            iterations=iterations,
            measure_time=True
        )
        print(f"{iterations:10d} | {results['time_seconds']:8.3f} | {results['iterations_per_second']:8.0f}")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("POKER ENGINE TEST SUITE")
    print("=" * 50)
    
    test_card_creation()
    test_deck_dealing()
    test_hand_evaluation()
    test_monte_carlo()
    test_monte_carlo_with_timing()
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()