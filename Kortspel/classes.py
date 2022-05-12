from random import shuffle

class Card:
	def __init__(self, suit, value, index_value):
		self.suit = suit
		self.value = value
		self.index_value = index_value

	def __str__(self):
		return(f"{self.suit}{self.value}")

class Deck:
	def __init__(self, to_shuffle = True):
		self.generate_deck(to_shuffle)

	def generate_deck(self, to_shuffle = True):
		temp_deck = []
		for suit in "HSDC":
			for index, value in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]):
				temp_deck.append(Card(suit, value, index))
		self.deck = temp_deck
		if to_shuffle:
			shuffle(self.deck)

	def __str__(self):
		return ", ".join(str(card) for card in self.deck)

	def shuffle_deck(self):
		shuffle(self.deck)

	def take_card(self):
		return self.deck.pop()