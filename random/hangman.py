import numpy as np
import os, random, sys

board = np.array([[" " for j in range(36)] for i in range(25)])
lengthOfBoard = len(board[0])
guessesMade = 0
correctWord = ""
wordToShow = []
guessedLetters = []

def loadWordsFromFile(filename):
	with open(filename) as f:
		words = f.read().split("\n")
	return words

def createWordToShow(word):
	wordToShow = ["_" for i in range(len(word))]
	
def getNewWord(words):
	newWord = random.choice(words)
	createWordToShow(newWord)
	return random.choice(words)

def checkAndChangeWord(letter):
	if letter in guessedLetters or letter == " " or len(letter) != 1:
		return -1

	exists = False
	for i, val in enumerate(correctWord):
		if val == letter:
			exists = True
			wordToShow[i] = val

	guessedLetters.append(letter)
	if exists:
		return 1
	return 0

def editBoard(board, data):
	for char in data:
		board[char[0], char[1]] = char[2]

def printBoard(board):
	print("*"*(lengthOfBoard+2))
	print("*" + f"{f'Guess Word. Guesses Left: {guessesMade}':<{lengthOfBoard}}" + "*")
	print("*"*(lengthOfBoard+2))
	print("*" + f"{' '.join(word for word in wordToShow):^{lengthOfBoard}}" + "*")
	print("*"*(lengthOfBoard+2))
	for row in board:
		print("*"+"".join(r for r in row)+"*")
	print("*"*(lengthOfBoard+2))

model = [[[24, 0, '-'], [24, 1, '-'], [24, 2, '-'], [24, 3, '-'], [24, 4, '-'], [24, 5, '-'], [24, 6, '-'], [24, 7, '-'], [24, 8, '-'], [24, 9, '-'], [24, 10, '-'], [24, 11, '-']],
		[[23, 0, '/'], [22, 1, '/'], [21, 2, '/'], [20, 3, '/'], [19, 4, '/']],
		[[23, 11, '\\'], [22, 10, '\\'], [21, 9, '\\'], [20, 8, '\\'], [19, 7, '\\']],
		[[2, 5, '|'], [3, 5, '|'], [4, 5, '|'], [5, 5, '|'], [6, 5, '|'], [7, 5, '|'], [8, 5, '|'], [9, 5, '|'], [10, 5, '|'], [11, 5, '|'], [12, 5, '|'], [13, 5, '|'], [14, 5, '|'], [15, 5, '|'], [16, 5, '|'], [17, 5, '|'], [18, 5, '|'], [19, 5, '|'], [20, 5, '|'], [21, 5, '|'], [22, 5, '|'], [23, 5, '|'],
		[2, 6, '|'], [3, 6, '|'], [4, 6, '|'], [5, 6, '|'], [6, 6, '|'], [7, 6, '|'], [8, 6, '|'], [9, 6, '|'], [10, 6, '|'], [11, 6, '|'], [12, 6, '|'], [13, 6, '|'], [14, 6, '|'], [15, 6, '|'], [16, 6, '|'], [17, 6, '|'], [18, 6, '|'], [19, 6, '|'], [20, 6, '|'], [21, 6, '|'], [22, 6, '|'], [23, 6, '|']],
		[[1, 5, "/"], [0, 6, '_'], [0, 7, '_'], [0, 8, '_'], [0, 9, '_'], [0, 10, '_'], [0, 11, '_'], [0, 12, '_'], [0, 13, '_'], [0, 14, '_'], [0, 15, '_'], [0, 16, '_'], [0, 17, '_'], [1, 6, '_'], [1, 7, '_'], [1, 8, '_'], [1, 9, '_'], [1, 10, '_'], [1, 11, '_'], [1, 12, '_'], [1, 13, '_'], [1, 14, '_'], 
			[1, 15, '_'], [1, 16, '_'], [1, 17, '_'], [0, 18, '_'], [0, 19, '_'], [0, 20, '_'], [0, 21, '_'], [0, 22, '_'], [0, 23, '_'], [0, 24, '_'], [0, 25, '_'], [0, 26, '_'], [0, 27, '_'], [0, 28, '_'], [0, 29, '_'],
			[1, 18, '_'], [1, 19, '_'], [1, 20, '_'], [1, 21, '_'], [1, 22, '_'], [1, 23, '_'], [1, 24, '_'], [1, 25, '_'], [1, 26, '_'], [1, 27, '_'], [1, 28, '_'], [1, 29, '_'], [1, 30, "\\"]],
		[[2, 30, "|"], [2, 29, "|"], [3, 30, "|"], [3, 29, "|"], [4, 30, "|"], [4, 29, "|"]],
		[[5, 27, "-"],[5, 28, "-"], [5, 29, "-"], [5, 30, "-"], [5, 31, "-"], [5, 32, "-"], [6, 26, "/"], [6, 33, "\\"], [7, 25, "/"], [7, 34, "\\"], [8, 25, "\\"], [8, 34, "/"], [9, 26, "\\"], [9, 33, "/"], [10, 27, '-'], [10, 28, '-'], [10, 29, '-'], [10, 30, '-'], [10, 31, '-'], [10, 32, '-']],
		[[11, 29, "|"], [11, 30, "|"], [12, 29, "|"], [12, 30, "|"], [13, 29, "|"], [13, 30, "|"], [14, 29, "|"], [14, 30, "|"]],
		[[13, 31, "/"], [12, 32, "/"]],
		[[13, 28, "\\"], [12, 27, "\\"]],
		[[15, 31, "\\"], [16, 32, "\\"]],
		[[15, 28, "/"], [16, 27, "/"]]]


def homeScreen():
	print("Welcome to hangman.\nChoose option below")
	print("1. Use random word from file.")
	print("2. Choose word yourself.")
	print("3. Use standard words.")
	print("4. Use standard words.")

	chosen = False
	while not chosen:
		try:
			number = int(input("Answer: "))
			if number > 0 and number < 4:
				chosen = True
				break
			else:
				print("Please enter number between 1 and 3.")
		except ValueError:
			print("Please enter an integer.")
		except:
			print("Error occured, please try again.")
	return number

def handleAnswer(number):	
	if number == 1:
		filename = input("Please enter name of file: ")
		words = loadWordsFromFile(filename)
		correctWord = getNewWord(words)
	elif number == 2:
		pass
	elif number == 3:
		pass


def runGame():
	hasLost = False
	hasWon = False
	while not hasWon and not hasLost:
		os.system("cls")
		printBoard(board)
		answer = input("*Guess: ")
		check = checkAndChangeWord(answer.upper())
		if check == 0:
			editBoard(board, model[guessesMade])
			guessesMade += 1

if __name__ == "__main__":
	play = True
	while play:
		answer = homeScreen()
		handleAnswer(answer)
		runGame()