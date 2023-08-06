def start():
	prog = input("имя твоей програмы(где ты запускал эту библиотеку)")
	proga = open(prog,"a")
	inputcode = input("то что хочешь пока что это print или вывести, function или функция")
	if inputcode == "print":
		print()
	if inputcode == "function":
		func()
	proga.close()
def print():
	inpr = input("текст который выведится")
	proga.write("print(" + '"' + inpr + '"' + ") \n")

def func():
	namedef = input("имя функции")
	proga.write("def " + namedef + "(): \n")
	code = input("код внутри функции")
	proga.write("	" + code)