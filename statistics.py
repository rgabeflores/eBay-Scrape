import random as r
import re

options = ["(1) Test Random Numbers", "(2) Input Values"]

def mean(a):
	'''
		Gets the average of an array of numbers.
	'''

	total = 0

	for i in a:
		total += i

	return total / len(a)

def median(a):
	'''
		Implements Divide & Conquer technique to find the middle element of an array.
	'''
	a.sort()
	if len(a) % 2 == 0:
		return (a[int(len(a) / 2)] + a[int(len(a) / 2) - 1]) / 2
	else:
		return a[int(len(a) / 2)]

def mode(a):
	'''
		Finds the most commonly recurring element in an array.
		Returns None if there is no element with more than one isntance.
	'''
	totals = {"_" : 0}

	for i in a:
		if i in totals:
			totals[i] += 1
		else:
			totals[i] = 1

	temp = "_"

	for key in totals:
		if totals[key] > totals[temp]:
			temp = key

	if totals[temp] > 1:
		return temp
	else:
		return None


def std_dev(a, average=None, var=None):
	'''
		Finds the the standard deviation of elements in an array.
	'''
	if average is None:
		average = mean(a)
	if var is None:
		var = variance(a, average)

	return var ** 0.5

def variance(a, average=None):
	if average is None:
		average = mean(a)

	total = 0
	for i in a:
		total += (average - i) ** 2

	return total / len(a)

def get_user_choice():

	ui_menu = "\n\t"

	for option in options:
		ui_menu += option + "\n\t"

	while True:
		try:
			print(ui_menu)
			choice = int(input("\tEnter a function to use:  "))
			if choice <= len(options) and choice > 0:
				return choice
			else:
				raise ValueError("Number too large.")
		except ValueError as e:
			print("\n\n\tPlease enter a valid choice.\n")
			continue


def to_continue():
	while True:
		again = input("Would you like to try again? (Y/N)\n")
		if again.upper() == "Y":
			return True
		elif again.upper() == "N":
			return False
		else:
			print("\n\n\tPlease enter a valid option.\n")
			continue

def randomTest():

	n = int(input("\tEnter the size of the list to test: "))
	
	values = [r.randint(0,100) for i in range(n)]

	return values

def userInputTest():

	user_input = input("    Enter the values separated by commas or spaces: ")

	values = [int(x.strip()) for x in re.split(' |, |\n', user_input)]

	return values

def main():

	cont = True

	while cont:
		
		choice = get_user_choice()

		print("\n")
		
		if choice == 1:
			values = randomTest()
		elif choice == 2:
			values = userInputTest()

		print("\n\tValues:", values,"\n")
		values.sort()
		print("\n\tValues Sorted: ", values)

		_high = values[len(values) - 1]
		_low = values[0]
		_mean = mean(values)
		_median = median(values)
		_mode = mode(values)
		_variance = variance(values, average=_mean)
		_std_dev = std_dev(values, average=_mean, variance=_variance)

		print("\tHigh", _high)
		print("\tLow", _low)
		print("\tMean:", _mean)
		print("\tMedian:", _median)
		print("\tMode:", _mode)
		print("\tVariance:", _variance)
		print("\tStandard Deviation:", _std_dev)
		print("\n\n")

		cont = to_continue()

	print("\n\n")

if __name__ == "__main__":
	main()