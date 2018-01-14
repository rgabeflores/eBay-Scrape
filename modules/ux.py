def get_user_choice(options):
	'''
		Takes a list or tuple of strings and displays them adjacent to numbers
		to emulate a menu interface and returns an Integer input taken from user.
	'''
	ui_menu = "\n\t"

	for i in range(len(options)):
		ui_menu += "(" + str(i + 1) + ")" + " " + str(options[i]) + "\n\t"

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


def to_continue(main):
	'''
		A continuous loop wrapper for a main function. Takes a function as a parameter.
		Useful for providing scripts with the option to run multiple times.
	'''
	cont = True
	while cont:

		main()

		while True:
			again = input("Would you like to try again? (Y/N)\n")
			if again.upper() == "Y":
				break
			elif again.upper() == "N":
				cont = False
				break
			else:
				print("\n\n\tPlease enter a valid option.\n")
				continue

	print("\n\n")
