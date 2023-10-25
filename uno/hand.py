from card import Card

class Hand:
    """Рука игрока"""
    def __init__(self, cardlist: list[Card]):
        self.card = cardlist

    def __repr__(self):
        """r4 y9 b1 b0"""
        return ' '.join([str(c) for c in self.cards])

    def __len__(self):
        """Возвращает размер руки"""
        return len(self.cards)

    def __getitem__(self, item):
        """Даёт hand[i]  и hard[i:j]"""
        return

    def get_playable_cards(self, topcard: Card):
        """Возвращает список карт, которые можно было бы сыграть на topcard"""
        return [card for card in self.cards if topcard.accept(card)]

    def remove_card(self, card: Card):
        """удаляет из руки карту card (чтобы положит её в отбой)"""
        self.cards = [c for c in self.cards if c != card]