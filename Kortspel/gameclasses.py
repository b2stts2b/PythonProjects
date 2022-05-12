from classes import *
import os

class Idiot:
	def __init__(self):
		self.deck = Deck(True)
		self.MESSAGE = ["[N]/[n] : Next round\n",
						"[R]/[r] : Auto remove\n",
						"[Rx]/[rx] : Remove card on pile x (1-4).\n",
						"[Mxy]/[mxy] : Move card on pile x to pile y."]


	def __str__(self):
		return str(self.deck)

	# Main game loop
	def game(self):
		piles = [[], [], [], []]
		
		# Let user play each round
		for game_round in range(13):
			self.take_new_cards(piles)

			# Loop until user wants more cards (input "N")
			while True:
				self.clear()
				self.print_piles(piles)
				print("\nWhat do you want to do?\n" + "".join(self.MESSAGE))
				answer = input("Answer: ").lower()

				# Execute what user wants
				# New Round or auto remove
				if len(answer) == 1:
					if answer == "n":
						break
					if answer == "r":
						for pos in range(4):
							if self.can_remove(piles, pos):
								piles[pos].pop()
								break		
				# Remove Card
				if len(answer) == 2:
					if answer[0] == "r":
						if answer[1].isdigit():
							pos = int(answer[1])-1
							if pos >= 0 and pos <= 3:
								if self.can_remove(piles, pos):
									piles[pos].pop()
				# Move Card
				if len(answer) == 3:
					if answer[0] == "m":
						if answer[1].isdigit() and answer[2].isdigit():
							x, y = int(answer[1])-1, int(answer[2])-1
							if len(piles[y]) == 0 and len(piles[x]) > 0:
								piles[y].append(piles[x].pop())

		print(f"YOUR SCORE IS: {sum([len(piles[0]), len(piles[1]), len(piles[2]), len(piles[3])])}")
	# Add new cards to piles
	def take_new_cards(self, piles):
		for i in range(4):
			piles[i].append(self.deck.take_card())

	# Check if card in position can be removed
	def can_remove(self, piles, pos):
		# No cards where we want to remove
		if len(piles[pos]) == 0:
			return False

		# Check if other piles have higher card
		for pile_index, cards in enumerate(piles):
			if len(cards) > 0:
				if cards[-1].suit == piles[pos][-1].suit:
					if cards[-1].index_value > piles[pos][-1].index_value:
						return True
		return False

	# Clear the terminal
	def clear(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	# Print out the piles
	def print_piles(self, piles):
		# Check length of longest pile
		max_length = 0
		for pile in piles:
			max_length = max(max_length, len(pile))

		# Print the piles to terminal
		for i in range(0, max_length, 1):
			print("|", end="")
			for pile in piles:
				if len(pile)+i >= max_length:
					print(f"{str(pile[len(pile)-max_length+i]):<3}|", end="")
				else:
					print("   |", end="")
			print()