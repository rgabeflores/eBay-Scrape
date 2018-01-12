def get_user_choice(options):

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
