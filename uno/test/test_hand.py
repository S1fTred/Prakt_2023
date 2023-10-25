from card import Card
from deck import Deck
from hand import Hand

def test_hand():
    text = 'r4 y9 b1 b0'
    hand = Hand(Card.card_list(text))
    assert text == str(hand)

def test_acceptable_list():
    text = 'r4 y9 g1 b0'
    hand = Hand(Card.card_list(text))

    # только одна карта
    cl = hand.get_playable_cards(Card('green', 5))
    assert cl == [Card.create('g1')]

    # Две карты
    cl = hand.get_playable_cards(Card('green', 9))
    assert cl == [Card.create('g1'), Card.create('y9')]

def test_no_playable_cards():
    text = 'r4 y9 g1'
    hand = Hand(Card.card_list(text))

    cl = hand.get_playable_cards(Card('blue', 5))
    assert cl == []

