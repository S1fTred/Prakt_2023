from card import Card
from deck import Deck



def test_deck():
    text = 'r4 y9 b1 b0'
    card_list = Card.card_list(text)
    deck = Deck(card_list)
    assert text == str(deck)


def test_draw():
    text = 'r4 y9 b1 b0'
    deck = Deck(Card.card_list(text))
    assert text == str(deck)

    c = deck.draw()
    assert ' r43 y9 b1' == str(deck)
    assert c == Card('blue', 1)

