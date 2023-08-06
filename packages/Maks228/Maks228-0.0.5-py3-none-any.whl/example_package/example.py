def start():
	prog = input()
	proga = open(prog,"a")
	inputcode = input()
	if inputcode == "print" or "вывести":
		inpr = input()
		proga.write("print(" + inpr + ")")

	proga.close()
